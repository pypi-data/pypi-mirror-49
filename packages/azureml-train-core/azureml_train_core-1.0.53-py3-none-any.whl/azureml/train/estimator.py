# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Definition for the generic Estimator classes.

Estimators are the building block for training.  An estimator encapsulates the training code and parameters,
the compute resources and runtime environment for a particular training scenario.

With Azure Machine Learning, you can easily submit your training script to various compute targets, using
:class:`azureml.core.runconfig.RunConfiguration` object and :class:`azureml.core.script_run_config.ScriptRunConfig`
object. That pattern gives you a lot of flexibility and maximum control.

To facilitate deep learning model training, the Azure Machine Learning Python SDK provides an alternative
higher-level abstraction, the estimator, which allows users to easily construct run configurations. You can create
and use a generic :class:`azureml.train.estimator.Estimator` to submit a training script using any learning framework
you choose. You can submit your run on any compute target, whether it's your local machine,
a single VM in Azure, or a GPU cluster in Azure. For PyTorch, TensorFlow, Chainer, and Scikit-learn tasks,
Azure Machine Learning also provides :class:`azureml.train.dnn.PyTorch`, :class:`azureml.train.dnn.TensorFlow`,
:class:`azureml.train.dnn.Chainer`, and :class:`azureml.train.sklearn.SKLearn` estimators respectively to simplify
using these frameworks.

For introduction to model training, please see
https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-train-ml-models

For information about docker containers used in Azure ML training, please see
https://github.com/Azure/AzureML-Containers

"""

from os import path, listdir
import logging
import ruamel.yaml

from azureml.core._experiment_method import experiment_method
from azureml.core.runconfig import TensorflowConfiguration, MpiConfiguration, RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute import AmlCompute
from azureml.core.experiment import Experiment
from azureml.core.script_run_config import ScriptRunConfig
from azureml.exceptions import TrainingException, AzureMLException
from azureml._base_sdk_common.utils import merge_dict, convert_list_to_dict
from azureml._base_sdk_common import _ClientSessionId
from azureml.train._telemetry_logger import _TelemetryLogger
from ._estimator_helper import _estimator_submit_method, _init_run_config, \
    _get_arguments, _get_data_inputs, _get_data_references, \
    _is_notebook_run, _update_config_for_notebook_run, _is_user_managed_environment

import uuid
import json
from abc import ABC

module_logger = logging.getLogger(__name__)


class MMLBaseEstimator(ABC):
    """Abstract base class for all estimators."""

    # these instance variables are added here to enable the use of mock objects in testing
    run_config = None
    _compute_target = None
    _estimator_config = None
    _original_config = None

    def __init__(self, source_directory, *, compute_target, estimator_config=None):
        """Initialize properties common to all estimators.

        :param source_directory: The directory containing code or configuration for the estimator.
        :type source_directory: str
        :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param estimator_config: The run-time configuration used by the estimator.
        :type estimator_config: azureml.core.runconfig.RunConfiguration
        """
        self._source_directory = source_directory if source_directory else "."
        self._compute_target = compute_target
        self._estimator_config = estimator_config
        self._logger = _TelemetryLogger.get_telemetry_logger(__name__)

    @property
    def source_directory(self):
        """Return the path to the source directory.

        :return: The source directory path.
        :rtype: str
        """
        return self._source_directory

    @property
    def run_config(self):
        """Return `RunConfiguration` object for this estimator.

        :return: The run configuration.
        :rtype: azureml.core.runconfig.RunConfiguration
        """
        return self._estimator_config

    @property
    def conda_dependencies(self):
        """Return `conda_dependencies` object for this estimator.

        :return: The conda dependencies.
        :rtype: azureml.core.conda_dependencies.CondaDependencies
        """
        return self.run_config.environment.python.conda_dependencies

    def _get_script_run_config(self, activity_logger=None, telemetry_values=None):
        script = self.run_config.script
        if _is_notebook_run(script):
            if activity_logger is not None:
                activity_logger.info("Training script is a notebook")
            # Since notebook runs are in preview, the dependencies are in contrib package
            # If a user is using notebook run, check if the required contrib package is installed.
            # This is a temp check. Once it is moved out of contrib, no need for this check.
            try:
                from azureml.contrib.notebook import NotebookRunConfig
            except ImportError:
                raise TrainingException("To use a jupyter notebook for training script install notebook"
                                        "dependencies from azureml-contrib-notebook. PyPi information "
                                        "for this package can be found at "
                                        "https://pypi.org/project/azureml-contrib-notebook/")
            return NotebookRunConfig(source_directory=self.source_directory,
                                     notebook=self.run_config.script,
                                     parameters=convert_list_to_dict(self.run_config.arguments),
                                     run_config=self.run_config,
                                     output_notebook="./outputs/{}.output.ipynb".format(
                                         script.split(".ipynb")[0]),
                                     _telemetry_values=telemetry_values)
        else:
            return ScriptRunConfig(source_directory=self.source_directory,
                                   script=self.run_config.script, arguments=self.run_config.arguments,
                                   run_config=self.run_config, _telemetry_values=telemetry_values)

    def _submit(self, workspace, experiment_name, telemetry_values):
        # For flag based script arguments with store_action attr,
        # the expected input to estimator script_params is {"--v": ""}
        # The script_params gets translated into list as ["--v", ""].
        # Remove the empty entry from the list before submitting the experiment.
        with _TelemetryLogger.log_activity(self._logger,
                                           "train.estimator.submit",
                                           custom_dimensions=telemetry_values) as activity_logger:
            try:
                activity_logger.info("Submitting experiment through estimator...")
                experiment = Experiment(workspace, experiment_name)
                config = self._get_script_run_config(activity_logger, telemetry_values)
                experiment_run = experiment.submit(config)
                activity_logger.info("Experiment was submitted. RunId=%s", experiment_run.id)

                return experiment_run
            except AzureMLException as e:
                raise TrainingException(e.message, inner_exception=e) from None

    def _fit(self, workspace, experiment_name):
        telemetry_values = self._get_telemetry_values(self._fit)
        self._last_submitted_runconfig = self.run_config

        return self._submit(workspace, experiment_name, telemetry_values)

    def _override_params(self, script_params=None, inputs=None, source_directory_data_store=None):
        data_inputs = []
        if script_params:
            merged_script_params = merge_dict(convert_list_to_dict(self._estimator_config.arguments), script_params)
            self._estimator_config.arguments = _get_arguments(merged_script_params)
            data_inputs = _get_data_inputs(script_params)

        data_references = _get_data_references(inputs, data_inputs, source_directory_data_store)
        self._estimator_config.data_references = merge_dict(self._estimator_config.data_references, data_references)
        if source_directory_data_store:
            self._estimator_config.source_directory_data_store = source_directory_data_store.name

    def _get_telemetry_values(self, func):
        _azureml_supported_framework_packages = ("tensorflow", "torch", "chainer", "scikit-learn")
        telemetry_values = {}

        # client common...
        telemetry_values['amlClientType'] = 'azureml-sdk-train'
        telemetry_values['amlClientFunction'] = func.__name__
        telemetry_values['amlClientModule'] = self.__class__.__module__
        telemetry_values['amlClientClass'] = self.__class__.__name__
        telemetry_values['amlClientRequestId'] = str(uuid.uuid4())
        telemetry_values['amlClientSessionId'] = _ClientSessionId

        # estimator related...
        telemetry_values['scriptName'] = self.run_config.script
        telemetry_values['scriptArguments'] = ' '.join(str(arg) for arg in self.run_config.arguments)
        telemetry_values['useGpu'] = self.run_config.environment.docker.gpu_support
        telemetry_values['useDocker'] = self.run_config.environment.docker.enabled
        telemetry_values['useCustomDockerImage'] = not (
            self.run_config.environment.docker.base_image.lower().startswith('mcr.microsoft.com/azureml/base') or
            (self.run_config.environment.docker.base_image_registry.address is not None and
             self.run_config.environment.docker.base_image_registry.address.startswith('viennaprivate.azurecr.io')))
        telemetry_values['addCondaOrPipPackage'] = self.conda_dependencies.serialize_to_string() != \
            CondaDependencies().serialize_to_string()
        telemetry_values['IsFrameworkPipPackageAdded'] = True \
            if len([p for p in self.conda_dependencies.pip_packages if
                    p.lower().startswith(_azureml_supported_framework_packages)]) else False
        telemetry_values['IsFrameworkCondaPackageAdded'] = True \
            if len([p for p in self.conda_dependencies.conda_packages if
                    p.lower().startswith(_azureml_supported_framework_packages)]) else False

        # data references related...
        data_references = self.run_config.data_references
        count_value = {}
        count_value['total'] = len(data_references)
        for key, value in data_references.items():
            if value.mode not in count_value:
                count_value[value.mode] = 0
            count_value[value.mode] += 1
        telemetry_values['amlDataReferences'] = json.dumps(count_value)
        telemetry_values['amlDataReferencesEnabled'] = len(data_references) > 0

        # distributed training related...
        telemetry_values['nodeCount'] = self._estimator_config.node_count
        telemetry_values['processCountPerNode'] = self.run_config.mpi.process_count_per_node

        telemetry_values['manualRestart'] = self._manual_restart_used

        if self._distributed_backend:
            if isinstance(self._distributed_backend, str):
                telemetry_values['distributed_backend'] = self._distributed_backend
            elif isinstance(self._distributed_backend, TensorflowConfiguration):
                telemetry_values['distributed_backend'] = "ps"
            elif isinstance(self._distributed_backend, MpiConfiguration):
                telemetry_values['distributed_backend'] = "mpi"

        telemetry_values['computeTarget'] = self._compute_target if isinstance(self._compute_target, str) else \
            self._compute_target.type if self._compute_target else "amlcompute"
        telemetry_values['vmSize'] = self.run_config.amlcompute.vm_size if self.run_config.amlcompute \
            else None
        telemetry_values['shmSize'] = self.run_config.environment.docker.shm_size

        return telemetry_values

    @classmethod
    def _get_supported_backends(cls):
        """
        Return the distributed training backend(s) supported by the estimator class.

        :return: The supported backend(s).
        :rtype: list
        """
        return cls._SUPPORTED_BACKENDS


class MMLBaseEstimatorRunConfig(RunConfiguration):
    """
    Abstract base class for all Estimator run configs.

    :param compute_target: The ComputeTarget where training will happen. This can either be an object or the
        string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.

        Supported values: Any Azure VM size.

        The list of available VM sizes are listed here:
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.

        Supported values: 'dedicated' and 'lowpriority'.

        This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dictionary containing parameters that will be passed as arguments to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. Only AmlCompute target
        is supported for distributed training (node_count > 1).
    :type node_count: int
    :param process_count_per_node: When using MPI as an execution backend, the number of processes per node.
    :type process_count_per_node: int
    :param distributed_backend: Communication backend for distributed training.

        Supported values: 'mpi' and 'ps'.

            'mpi': MPI/Horovod
            'ps': parameter server

        This parameter is required when any of node_count, process_count_per_node, worker_count, or
        parameter_server_count > 1.

        When node_count == 1 and process_count_per_node == 1, no backend will be used unless the backend
        is explicitly set. Only AmlCompute target is supported for distributed training.
    :type distributed_backend: str
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.container_registry.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonSection and DockerSection and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: The backing data store for the project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the Docker container's shared memory block. Please refer to
        https://docs.docker.com/engine/reference/run/ for more information. If not set, default is 1G.
    :type shm_size: str
    """

    def __init__(self, compute_target, vm_size=None, vm_priority=None,
                 entry_script=None, script_params=None, node_count=None,
                 process_count_per_node=None, distributed_backend=None, use_gpu=None, use_docker=None,
                 custom_docker_image=None, image_registry_details=None, user_managed=False, conda_packages=None,
                 pip_packages=None, environment_definition=None, inputs=None, source_directory_data_store=None,
                 shm_size=None):
        """Initialize the MMLBaseEstimatorRunConfig."""
        module_logger.warning("'MMLBaseEstimatorRunConfig' will be deprecated soon. Please "
                              "use 'azureml.core.runconfig.RunConfiguration'.")

        estimator_config = _init_run_config(estimator=None,
                                            source_directory=None,
                                            compute_target=compute_target,
                                            vm_size=vm_size,
                                            vm_priority=vm_priority,
                                            entry_script=entry_script,
                                            script_params=script_params,
                                            node_count=node_count,
                                            process_count_per_node=process_count_per_node,
                                            distributed_backend=distributed_backend,
                                            use_gpu=use_gpu,
                                            use_docker=use_docker,
                                            custom_docker_image=custom_docker_image,
                                            image_registry_details=image_registry_details,
                                            user_managed=user_managed,
                                            conda_packages=conda_packages,
                                            pip_packages=pip_packages,
                                            environment_definition=environment_definition,
                                            inputs=inputs,
                                            source_directory_data_store=source_directory_data_store,
                                            shm_size=shm_size)

        self.__dict__.update(estimator_config.__dict__)


class Estimator(MMLBaseEstimator):
    """A generic Estimator to train the data using any supplied framework.

    This class is designed for use with frameworks that do not have a framework specific estimator class.

    .. remarks::
            This simple estimator wraps run configuration information to help simplify the tasks of specifying
            how a script is executed. It supports single-node as well as multi-node execution. Execution of the
            estimator will result in a model being produced which should be placed in the
            ScriptParams.OUTPUT_PATH folder.

            An example of how to submit an experiment through Estimator:

            .. code-block:: python

                from azureml.train.estimator import Estimator

                # run an experiment from the train.py code in your current directory
                estimator = Estimator(source_directory='.',
                                      compute_target='local',
                                      entry_script='train.py',
                                      conda_packages=['scikit-learn'])

                # submit the experiment and then wait until complete
                run = experiment.submit(estimator)
                run.wait_for_completion()

            See https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-train-models-with-aml
            for an example of training a model using remote cluster through Estimator.

            For information about docker containers used in Azure ML training, please see
            https://github.com/Azure/AzureML-Containers

    :param source_directory: A local directory containing experiment configuration files.
    :type source_directory: str
    :param compute_target:  The ComputeTarget where training will happen. This can either be an object or the
        string "local".
    :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
    :param vm_size: The VM size of the compute target that will be created for the training.

        Supported values: Any Azure VM size.

        The list of available VM sizes are listed here:
        https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
    :type vm_size: str
    :param vm_priority: The VM priority of the compute target that will be created for the training. If not
        specified, it will be defaulted to 'dedicated'.

        Supported values: 'dedicated' and 'lowpriority'.

        This takes effect only when the vm_size param is specified in the input.
    :type vm_priority: str
    :param entry_script: A string representing the relative path to the file used to start training.
    :type entry_script: str
    :param script_params: A dictionary containing parameters to the entry_script.
    :type script_params: dict
    :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
         distributed job will be run. Only AmlCompute target is supported for distributed jobs.
    :type node_count: int
    :param process_count_per_node: Number of processes per node. If greater than 1, mpi
         distributed job will be run. Only AmlCompute target is supported for distributed jobs.
    :type process_count_per_node: int
    :param distributed_backend: Communication backend for distributed training.

        Supported values: 'mpi'.

            'mpi': MPI/Horovod

        This parameter is required when node_count, process_count_per_node and/or worker_count > 1.

        When node_count == 1 and process_count_per_node == 1, no backend will be used
        unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
    :type distributed_backend: str
    :param distributed_training: Parameters for running a distributed training job. Please use this option
        instead of deprecated distributed_backend.

        For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
        object to specify process_count_per_node.
    :type distributed_training: azureml.core.runconfig.MpiConfiguration
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
    :type use_docker: bool
    :param custom_docker_image: The name of the docker image from which the image to use for training
        will be built. If not set, a default CPU based image will be used as the base image.
    :type custom_docker_image: str
    :param image_registry_details: The details of the docker image registry.
    :type image_registry_details: azureml.core.container_registry.ContainerRegistry
    :param user_managed: True means that AzureML reuses an existing python environment, False means
        that AzureML will create a python environment based on the Conda dependencies specification.
    :type user_managed: bool
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param conda_dependencies_file_path: A string representing the relative path to the conda dependencies yaml file.
    :type conda_dependencies_file_path: str
    :param pip_requirements_file_path: A string representing the relative path to the pip requirements text file.
        This can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file_path: str
    :param conda_dependencies_file: A string representing the relative path to the conda dependencies yaml file.
    :type conda_dependencies_file: str
    :param pip_requirements_file: A string representing the relative path to the pip requirements text file.
        This can be provided in combination with the pip_packages parameter.
    :type pip_requirements_file: str
    :param environment_variables: A dictionary of environment variables names and values.
        These environment variables are set on the process where user script is being executed.
    :type environment_variables: dict
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonSection and DockerSection and environment variables. Any environment option not directly
        exposed through other parameters to the Estimator construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    :param inputs: Data references as input.
    :type inputs: list
    :param source_directory_data_store: The backing data store for the project share.
    :type source_directory_data_store: str
    :param shm_size: The size of the Docker container's shared memory block. Please refer to
        https://docs.docker.com/engine/reference/run/ for more information. If not set, default is 1G.
    :type shm_size: str
    :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
    :type resume_from: azureml.data.datapath.DataPath
    :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
        cancel the run, if it took longer than this value.
    :type max_run_duration_seconds: int
    """

    _SUPPORTED_BACKENDS = ["mpi"]

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 distributed_backend=None,
                 distributed_training=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 conda_dependencies_file_path=None,
                 pip_requirements_file_path=None,
                 conda_dependencies_file=None,
                 pip_requirements_file=None,
                 environment_variables=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None,
                 resume_from=None,
                 max_run_duration_seconds=None):
        """Initialize the estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target:  The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.

            Supported values: Any Azure VM size.

            The list of available VM sizes are listed here:
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.

            Supported values: 'dedicated' and 'lowpriority'.

            This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dictionary containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param distributed_backend: Communication backend for distributed training.

            Supported values: 'mpi'.

                'mpi': MPI/Horovod

            This parameter is required when node_count, process_count_per_node and/or worker_count > 1.

            When node_count == 1 and process_count_per_node == 1, no backend will be used
            unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param distributed_training: Parameters for running a distributed training job. Please use this option
            instead of deprecated distributed_backend.

            For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
            object to specify process_count_per_node.
        :type distributed_training: azureml.core.runconfig.MpiConfiguration
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.container_registry.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param conda_dependencies_file_path: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file_path: str
        :param pip_requirements_file_path: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
         :param conda_dependencies_file: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file: str
        :param pip_requirements_file: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file: str
        :param environment_variables: A dictionary of environment variables names and values.
            These environment variables are set on the process where user script is being executed.
        :type environment_variables: dict
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonSection and DockerSection and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: The backing data store for the project share.
        :type source_directory_data_store: Datastore
        :param shm_size: The size of the Docker container's shared memory block. Please refer to
            https://docs.docker.com/engine/reference/run/ for more information. If not set, default is 1G.
        :type shm_size: str
        :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
            cancel the run, if it took longer than this value.
        :type max_run_duration_seconds: int
        """
        estimator_config = _init_run_config(
            estimator=self,
            source_directory=source_directory,
            compute_target=compute_target,
            vm_size=vm_size,
            vm_priority=vm_priority,
            entry_script=entry_script,
            script_params=script_params,
            node_count=node_count,
            process_count_per_node=process_count_per_node,
            distributed_backend=distributed_backend,
            distributed_training=distributed_training,
            use_gpu=use_gpu,
            use_docker=use_docker,
            custom_docker_image=custom_docker_image,
            image_registry_details=image_registry_details,
            user_managed=user_managed,
            conda_packages=conda_packages,
            pip_packages=pip_packages,
            conda_dependencies_file_path=conda_dependencies_file_path,
            pip_requirements_file_path=pip_requirements_file_path,
            conda_dependencies_file=conda_dependencies_file,
            pip_requirements_file=pip_requirements_file,
            environment_variables=environment_variables,
            environment_definition=environment_definition,
            inputs=inputs,
            source_directory_data_store=source_directory_data_store,
            shm_size=shm_size,
            resume_from=resume_from,
            max_run_duration_seconds=max_run_duration_seconds)

        self._manual_restart_used = (resume_from is not None)
        self._distributed_backend = distributed_backend
        if distributed_training:
            self._distributed_backend = distributed_training

        if _is_notebook_run(estimator_config.script):
            _update_config_for_notebook_run(estimator_config,
                                            use_gpu,
                                            custom_docker_image)

        super(self.__class__, self).__init__(source_directory, compute_target=compute_target,
                                             estimator_config=estimator_config)


class _FrameworkBaseEstimator(MMLBaseEstimator):
    """_FrameworkBaseEstimator is the base class of machine learning framework estimators."""

    _ACR_ADDRESS = 'viennaprivate.azurecr.io'
    _UNSUPPORTED_FRAMEWORK_VERSION_ERROR = \
        '{name} {version} is not currently supported by the {name} estimator. ' \
        'Check https://docs.microsoft.com/en-us/python/api/azureml-train-core/azureml.train.dnn?view=azure-ml-py ' \
        'for all supported versions. To use {name} {version}, switch to the generic Estimator class for your ' \
        'experiment.'
    _SCENARIO_FILE_NOT_FOUND_ERROR = 'Scenario file for {name}:{version} not found.'
    _EMPTY_FRAMEWORK_VERSION_WARNING = 'framework_version is not specified, defaulting to version {}.'
    _OPTIMIZED_MODE_PREVIEW_NOTICE = 'Note: Optimized Mode has been enabled. When additional packages are ' \
                                     'provided, pre-built framework image instead of default base image will ' \
                                     'be used as an intermediate image to build the final environment. '\
                                     'You can expect faster image building with this mode turned on. '\
                                     'This feature is currently in private preview.'

    FRAMEWORK_NAME = None
    DEFAULT_VERSION = None

    @experiment_method(submit_function=_estimator_submit_method)
    def __init__(self,
                 source_directory,
                 *,
                 compute_target=None,
                 vm_size=None,
                 vm_priority=None,
                 entry_script=None,
                 script_params=None,
                 node_count=1,
                 process_count_per_node=1,
                 distributed_backend=None,
                 distributed_training=None,
                 use_gpu=False,
                 use_docker=True,
                 custom_docker_image=None,
                 image_registry_details=None,
                 user_managed=False,
                 conda_packages=None,
                 pip_packages=None,
                 conda_dependencies_file_path=None,
                 pip_requirements_file_path=None,
                 conda_dependencies_file=None,
                 pip_requirements_file=None,
                 environment_variables=None,
                 environment_definition=None,
                 inputs=None,
                 source_directory_data_store=None,
                 shm_size=None,
                 resume_from=None,
                 max_run_duration_seconds=None,
                 framework_name=None,
                 framework_version=None,
                 _enable_optimized_mode=False):
        """Initialize the estimator.

        :param source_directory: A local directory containing experiment configuration files.
        :type source_directory: str
        :param compute_target:  The ComputeTarget where training will happen. This can either be an object or the
            string "local".
        :type compute_target: azureml.core.compute_target.AbstractComputeTarget or str
        :param vm_size: The VM size of the compute target that will be created for the training.

            Supported values: Any Azure VM size.

            The list of available VM sizes are listed here:
            https://docs.microsoft.com/en-us/azure/cloud-services/cloud-services-sizes-specs
        :type vm_size: str
        :param vm_priority: The VM priority of the compute target that will be created for the training. If not
            specified, it will be defaulted to 'dedicated'.

            Supported values: 'dedicated' and 'lowpriority'.

            This takes effect only when the vm_size param is specified in the input.
        :type vm_priority: str
        :param entry_script: A string representing the relative path to the file used to start training.
        :type entry_script: str
        :param script_params: A dictionary containing parameters to the entry_script.
        :type script_params: dict
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
             distributed job will be run. Only AmlCompute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param distributed_backend: Communication backend for distributed training.

            Supported values: 'mpi' and 'ps'.

                'mpi': MPI/Horovod
                'ps': parameter server

            This parameter is required when any of node_count, process_count_per_node, worker_count, or
            parameter_server_count > 1.
            In case of 'ps', worker_count + parameter_server_count should be less than or equal to
            node_count * (number of CPUs or GPUs per node)

            When node_count == 1 and process_count_per_node == 1, no backend will be used
            unless the backend is explicitly set. Only AmlCompute compute target is supported for distributed training.
        :type distributed_backend: str
        :param distributed_training: Parameters for running a distributed training job. Please use this option
            instead of deprecated distributed_backend.

            For running a distributed job with Parameter Server backend, use
            :class:`azureml.core.runconfig.TensorflowConfiguration` object to
            specify worker_count and parameter_server_count.
            worker_count + parameter_server_count should be less than or equal to
            node_count * (number of CPUs or GPUs per node)

            For running a distributed job with MPI backend, use :class:`azureml.core.runconfig.MpiConfiguration`
            object to specify process_count_per_node.
        :type distributed_training: azureml.core.runconfig.TensorflowConfiguration or
            azureml.core.runconfig.MpiConfiguration
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        :type use_docker: bool
        :param custom_docker_image: The name of the docker image from which the image to use for training
            will be built. If not set, a default CPU based image will be used as the base image.
        :type custom_docker_image: str
        :param image_registry_details: The details of the docker image registry.
        :type image_registry_details: azureml.core.container_registry.ContainerRegistry
        :param user_managed: True means that AzureML reuses an existing python environment, False means
            that AzureML will create a python environment based on the Conda dependencies specification.
        :type user_managed: bool
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param conda_dependencies_file_path: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file_path: str
        :param pip_requirements_file_path: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file_path: str
         :param conda_dependencies_file: A string representing the relative path to the conda dependencies
            yaml file.
        :type conda_dependencies_file: str
        :param pip_requirements_file: A string representing the relative path to the pip requirements text file.
            This can be provided in combination with the pip_packages parameter.
        :type pip_requirements_file: str
        :param environment_variables: A dictionary of environment variables names and values.
            These environment variables are set on the process where user script is being executed.
        :type environment_variables: dict
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonSection and DockerSection and environment variables. Any environment option not directly
            exposed through other parameters to the Estimator construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        :param inputs: Data references as input.
        :type inputs: list
        :param source_directory_data_store: The backing data store for the project share.
        :type source_directory_data_store: Datastore
        :param shm_size: The size of the Docker container's shared memory block. Please refer to
            https://docs.docker.com/engine/reference/run/ for more information. If not set, default is 1G.
        :type shm_size: str
        :param resume_from: DataPath containing the checkpoint or model files from which to resume the experiment.
        :type resume_from: azureml.data.datapath.DataPath
        :param max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically
            cancel the run, if it took longer than this value.
        :type max_run_duration_seconds: int
        :param framework_name: Name of the framework to be used for the estimator.
        :type framework_name: str
        :param framework_version: The version of the framework to be used for the estimator
        :type framework_version: str
        :param _enable_optimized_mode: Enable incremental environment build with pre-built framework images for faster
            environment preparation. A pre-built framework image is built on top of Azure ML default CPU/GPU base
            images with framework dependencies pre-installed.
        :type _enable_optimized_mode: bool
        """
        # For deprecation purposes
        if conda_dependencies_file:
            conda_output_str = "conda_dependencies_file"
        else:
            conda_output_str = "conda_dependencies_file_path"

        if environment_definition or (conda_dependencies_file_path or conda_dependencies_file):
            module_logger.warning("If environment_definition or {} is specified, Azure ML "
                                  "will not install any framework related packages on behalf of "
                                  "the user.".format(conda_output_str))

        self._optimized_mode = _enable_optimized_mode
        if self._optimized_mode:
            module_logger.warning(self._OPTIMIZED_MODE_PREVIEW_NOTICE)

        self._use_framework_image = False
        self._framework_name = framework_name if framework_name is not None else self.FRAMEWORK_NAME
        self._framework_version = framework_version

        self._estimator_config = \
            _init_run_config(estimator=self, source_directory=source_directory, compute_target=compute_target,
                             vm_size=vm_size, vm_priority=vm_priority, entry_script=entry_script,
                             script_params=script_params, node_count=node_count,
                             process_count_per_node=process_count_per_node, distributed_backend=distributed_backend,
                             distributed_training=distributed_training, use_gpu=use_gpu, use_docker=use_docker,
                             custom_docker_image=custom_docker_image, image_registry_details=image_registry_details,
                             user_managed=user_managed, conda_packages=conda_packages, pip_packages=pip_packages,
                             conda_dependencies_file_path=conda_dependencies_file_path,
                             pip_requirements_file_path=pip_requirements_file_path,
                             conda_dependencies_file=conda_dependencies_file,
                             pip_requirements_file=pip_requirements_file,
                             environment_variables=environment_variables,
                             environment_definition=environment_definition, inputs=inputs,
                             source_directory_data_store=source_directory_data_store, shm_size=shm_size,
                             resume_from=resume_from, max_run_duration_seconds=max_run_duration_seconds)

        if self.framework_version is None:
            self._framework_version = self.DEFAULT_VERSION
            if not self._estimator_config.environment.python.user_managed_dependencies and \
                    len(self.__class__.get_supported_versions()) > 1:
                module_logger.warning(self._EMPTY_FRAMEWORK_VERSION_WARNING.format(self.DEFAULT_VERSION))
        else:
            if framework_version not in self.__class__.get_supported_versions():
                raise TrainingException(self._UNSUPPORTED_FRAMEWORK_VERSION_ERROR.format(name=framework_name,
                                                                                         version=framework_version))

        if not conda_dependencies_file:
            conda_dependencies_file = conda_dependencies_file_path

        self._framework_processor = 'gpu' if self._estimator_config.environment.docker.gpu_support else 'cpu'
        self._manual_restart_used = (resume_from is not None)
        self._user_dependencies_provided = self.conda_dependencies.serialize_to_string() != \
            CondaDependencies().serialize_to_string()

        if not _is_user_managed_environment(environment_definition):
            self._check_package_conflicts()
            self._setup_environment(custom_docker_image, compute_target, entry_script,
                                    environment_definition, conda_dependencies_file)

        self._distributed_backend = distributed_backend
        if distributed_training:
            self._distributed_backend = distributed_training

        if _is_notebook_run(entry_script):
            _update_config_for_notebook_run(self._estimator_config, use_gpu,
                                            custom_docker_image)

        super().__init__(source_directory, compute_target=compute_target,
                         estimator_config=self._estimator_config)

    @property
    def framework_version(self):
        """
        Return the framework version.

        :return: The framework version.
        :rtype: str
        """
        return self._framework_version

    def _get_telemetry_values(self, func):
        telemetry_values = super()._get_telemetry_values(func)
        telemetry_values['frameworkVersion'] = self._framework_version
        telemetry_values['frameworkImageUsed'] = self._use_framework_image
        telemetry_values['incrementalBuild'] = self._estimator_config.environment.python. \
            _base_conda_environment is not None
        telemetry_values['addCondaOrPipPackage'] = self._user_dependencies_provided
        telemetry_values['manualRestart'] = self._manual_restart_used
        telemetry_values['isConflictPackagesAdded'] = self._is_conflict_package_added
        return telemetry_values

    def _load_from_scenario_file(self):
        # TODO: move file not found and parse error checks to gated tests
        scenario_filename = '{}-{}-{}.yml'.format(self._framework_name,
                                                  self._framework_version,
                                                  self._framework_processor).lower()
        scenario_path = path.join(path.dirname(__file__), "scenarios", scenario_filename)
        if not path.isfile(scenario_path):
            raise TrainingException((self._SCENARIO_FILE_NOT_FOUND_ERROR).
                                    format(name=self._framework_name, version=self._framework_version))
        with open(scenario_path, "r") as input:
            scenario = ruamel.yaml.round_trip_load(input)
            base_image = scenario.get('baseImage', None)
            dependencies = scenario.get('inlineCondaDependencies', None)

        return base_image, CondaDependencies(_underlying_structure=dependencies)

    def _setup_environment(self, custom_docker_image, compute_target, entry_script, environment_definition,
                           conda_dependencies_file):
        # check if framework image can be used
        self._use_framework_image = self._optimized_mode or not self._user_dependencies_provided

        if compute_target and not isinstance(compute_target, AmlCompute):
            self._use_framework_image = False
            if self._optimized_mode:
                raise TrainingException("Optimized mode is not supported for non-AmlCompute targets.")
        if environment_definition is not None or custom_docker_image is not None:
            self._use_framework_image = False
            if self._optimized_mode:
                raise TrainingException("Optimized mode is not supported when environment_definition "
                                        "or custom_docker_image is provided.")
        # Notebook runs are supported only in OpenMPI base images.
        # Current framework images use IntelMPI so they cannot be used.
        # Also, a full build is needed to install papermill dependencies.
        if _is_notebook_run(entry_script):
            self._use_framework_image = False
            if self._optimized_mode:
                raise TrainingException("Optimized mode is not supported when entry_script is a notebook "
                                        "file(.ipynb).")

        # setup the environment
        if self._use_framework_image:
            framework_image = '{}:{}-{}'.format(self._framework_name.lower(),
                                                self._framework_version,
                                                self._framework_processor)
            self._estimator_config.environment.docker.base_image = framework_image
            self._estimator_config.environment.docker.base_image_registry.address = self._ACR_ADDRESS
            if not self._user_dependencies_provided:
                # 1) no build - use framework image as final image
                self._estimator_config.environment.python.user_managed_dependencies = True
            else:
                # 2) incremental build - use framework image as base image
                self._estimator_config.environment.python._base_conda_environment = 'base'
        elif not environment_definition:
            # 3) full build
            default_base_image, framework_dependencies = self._load_from_scenario_file()
            # if conda_dependencies_file is specified, don't add framework dependencies
            if conda_dependencies_file is None:
                self.conda_dependencies._merge_dependencies(framework_dependencies)
            # if custom_docker_image or environment_definition is specified, don't override base image
            if custom_docker_image is None:
                self._estimator_config.environment.docker.base_image = default_base_image

    def _check_package_conflicts(self):
        self._is_conflict_package_added = False
        # Check if there are duplicate between packages that Azure ML installs and user specified packages.
        default_base_image, framework_dependencies = self._load_from_scenario_file()

        # Get all framework related packages installed by Azure ML
        # This will have default CondaDependencies() packages like azureml-defaults and framework related packages.
        framework_packages = []
        framework_packages.extend(
            [framework_dependencies._get_package_name(x) for x in framework_dependencies.pip_packages])
        framework_packages.extend(
            [framework_dependencies._get_package_name(x) for x in framework_dependencies.conda_packages])

        # Get all packages in estimator
        # This will have default CondaDependencies() packages like azureml-defaults and user specified packages.
        estimator_packages = []
        estimator_packages.extend(
            [self.conda_dependencies._get_package_name(x) for x in self.conda_dependencies.pip_packages])
        estimator_packages.extend(
            [self.conda_dependencies._get_package_name(x) for x in self.conda_dependencies.conda_packages])

        # Get default packages
        # This will help remove common packages between framework_packages and estimator_packages that
        # came from default CondaDependcies().
        default_packages = []
        default_packages.extend(
            [CondaDependencies()._get_package_name(x) for x in CondaDependencies().pip_packages])
        default_packages.extend(
            [CondaDependencies()._get_package_name(x) for x in CondaDependencies().conda_packages])

        common_packages = [p for p in estimator_packages if p in framework_packages and p not in default_packages]

        if len(common_packages):
            module_logger.warning("You have specified to install packages in your run. "
                                  "Note that Azure ML also installs the following packages on your behalf: {}. \n"
                                  "This may lead to unexpected package installation errors. "
                                  "Take a look at `estimator.conda_dependencies` to understand what packages are "
                                  "installed by Azure ML.".format([p for p in common_packages]))
            self._is_conflict_package_added = True

    @classmethod
    def get_supported_versions(cls):
        """
        Return the framework versions supported by the current SDK.

        :return: The supported framework versions.
        :rtype: list
        """
        framework_dir = path.join(path.dirname(__file__), "scenarios")
        dir_list = listdir(framework_dir)
        supported_versions = set([])

        for scenario_file in dir_list:
            if scenario_file.startswith(cls.FRAMEWORK_NAME.lower()):
                version = scenario_file.split('-')[1]
                supported_versions.add(version)

        return sorted(list(supported_versions))

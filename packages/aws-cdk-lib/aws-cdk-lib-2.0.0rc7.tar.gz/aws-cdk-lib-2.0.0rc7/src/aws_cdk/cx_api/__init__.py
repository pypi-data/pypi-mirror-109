'''
# Cloud Executable API

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from ..cloud_assembly_schema import (
    AmiContextQuery as _AmiContextQuery_74bf4b1b,
    ArtifactManifest as _ArtifactManifest_f79eef21,
    ArtifactType as _ArtifactType_1d870526,
    AssemblyManifest as _AssemblyManifest_413b9f23,
    AssetManifestProperties as _AssetManifestProperties_9084879a,
    AvailabilityZonesContextQuery as _AvailabilityZonesContextQuery_715a9fea,
    AwsCloudFormationStackProperties as _AwsCloudFormationStackProperties_50fb16af,
    ContainerImageAssetMetadataEntry as _ContainerImageAssetMetadataEntry_0a212d1d,
    ContextProvider as _ContextProvider_fa789bb5,
    EndpointServiceAvailabilityZonesContextQuery as _EndpointServiceAvailabilityZonesContextQuery_ea3ca0d1,
    FileAssetMetadataEntry as _FileAssetMetadataEntry_50173f8f,
    HostedZoneContextQuery as _HostedZoneContextQuery_8e6ca28f,
    LoadBalancerContextQuery as _LoadBalancerContextQuery_cb08d67c,
    LoadBalancerListenerContextQuery as _LoadBalancerListenerContextQuery_0eaf3c16,
    MetadataEntry as _MetadataEntry_13e1bf79,
    MissingContext as _MissingContext_0ff9e334,
    NestedCloudAssemblyProperties as _NestedCloudAssemblyProperties_c2fa342d,
    RuntimeInfo as _RuntimeInfo_3e9d9574,
    SSMParameterContextQuery as _SSMParameterContextQuery_675de122,
    SecurityGroupContextQuery as _SecurityGroupContextQuery_e772f3e6,
    Tag as _Tag_554dd7f9,
    TreeArtifactProperties as _TreeArtifactProperties_4092757e,
    VpcContextQuery as _VpcContextQuery_a193c650,
)


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.AssemblyBuildOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class AssemblyBuildOptions:
    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssemblyBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.AwsCloudFormationStackProperties",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "parameters": "parameters",
        "stack_name": "stackName",
        "termination_protection": "terminationProtection",
    },
)
class AwsCloudFormationStackProperties:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Artifact properties for CloudFormation stacks.

        :param template_file: (experimental) A file relative to the assembly root which contains the CloudFormation template for this stack.
        :param parameters: (experimental) Values for CloudFormation stack parameters that should be passed when the stack is deployed.
        :param stack_name: (experimental) The name to use for the CloudFormation stack. Default: - name derived from artifact ID
        :param termination_protection: (experimental) Whether to enable termination protection for this stack. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "template_file": template_file,
        }
        if parameters is not None:
            self._values["parameters"] = parameters
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection

    @builtins.property
    def template_file(self) -> builtins.str:
        '''(experimental) A file relative to the assembly root which contains the CloudFormation template for this stack.

        :stability: experimental
        '''
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Values for CloudFormation stack parameters that should be passed when the stack is deployed.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name to use for the CloudFormation stack.

        :default: - name derived from artifact ID

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable termination protection for this stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCloudFormationStackProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudArtifact(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.CloudArtifact",
):
    '''(experimental) Represents an artifact within a cloud assembly.

    :stability: experimental
    '''

    def __init__(
        self,
        assembly: "CloudAssembly",
        id: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''
        :param assembly: -
        :param id: -
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        manifest = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        jsii.create(CloudArtifact, self, [assembly, id, manifest])

    @jsii.member(jsii_name="fromManifest") # type: ignore[misc]
    @builtins.classmethod
    def from_manifest(
        cls,
        assembly: "CloudAssembly",
        id: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> typing.Optional["CloudArtifact"]:
        '''(experimental) Returns a subclass of ``CloudArtifact`` based on the artifact type defined in the artifact manifest.

        :param assembly: The cloud assembly from which to load the artifact.
        :param id: The artifact ID.
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :return: the ``CloudArtifact`` that matches the artifact type or ``undefined`` if it's an artifact type that is unrecognized by this module.

        :stability: experimental
        '''
        artifact = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        return typing.cast(typing.Optional["CloudArtifact"], jsii.sinvoke(cls, "fromManifest", [assembly, id, artifact]))

    @jsii.member(jsii_name="findMetadataByType")
    def find_metadata_by_type(
        self,
        type: builtins.str,
    ) -> typing.List["MetadataEntryResult"]:
        '''
        :param type: -

        :return: all the metadata entries of a specific type in this artifact.

        :stability: experimental
        '''
        return typing.cast(typing.List["MetadataEntryResult"], jsii.invoke(self, "findMetadataByType", [type]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assembly")
    def assembly(self) -> "CloudAssembly":
        '''
        :stability: experimental
        '''
        return typing.cast("CloudAssembly", jsii.get(self, "assembly"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["CloudArtifact"]:
        '''(experimental) Returns all the artifacts that this artifact depends on.

        :stability: experimental
        '''
        return typing.cast(typing.List["CloudArtifact"], jsii.get(self, "dependencies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hierarchicalId")
    def hierarchical_id(self) -> builtins.str:
        '''(experimental) An identifier that shows where this artifact is located in the tree of nested assemblies, based on their manifests.

        Defaults to the normal
        id. Should only be used in user interfaces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hierarchicalId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> _ArtifactManifest_f79eef21:
        '''(experimental) The artifact's manifest.

        :stability: experimental
        '''
        return typing.cast(_ArtifactManifest_f79eef21, jsii.get(self, "manifest"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="messages")
    def messages(self) -> typing.List["SynthesisMessage"]:
        '''(experimental) The set of messages extracted from the artifact's metadata.

        :stability: experimental
        '''
        return typing.cast(typing.List["SynthesisMessage"], jsii.get(self, "messages"))


class CloudAssembly(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.CloudAssembly",
):
    '''(experimental) Represents a deployable cloud application.

    :stability: experimental
    '''

    def __init__(self, directory: builtins.str) -> None:
        '''(experimental) Reads a cloud assembly from the specified directory.

        :param directory: The root directory of the assembly.

        :stability: experimental
        '''
        jsii.create(CloudAssembly, self, [directory])

    @jsii.member(jsii_name="getNestedAssembly")
    def get_nested_assembly(self, artifact_id: builtins.str) -> "CloudAssembly":
        '''(experimental) Returns a nested assembly.

        :param artifact_id: The artifact ID of the nested assembly.

        :stability: experimental
        '''
        return typing.cast("CloudAssembly", jsii.invoke(self, "getNestedAssembly", [artifact_id]))

    @jsii.member(jsii_name="getNestedAssemblyArtifact")
    def get_nested_assembly_artifact(
        self,
        artifact_id: builtins.str,
    ) -> "NestedCloudAssemblyArtifact":
        '''(experimental) Returns a nested assembly artifact.

        :param artifact_id: The artifact ID of the nested assembly.

        :stability: experimental
        '''
        return typing.cast("NestedCloudAssemblyArtifact", jsii.invoke(self, "getNestedAssemblyArtifact", [artifact_id]))

    @jsii.member(jsii_name="getStackArtifact")
    def get_stack_artifact(
        self,
        artifact_id: builtins.str,
    ) -> "CloudFormationStackArtifact":
        '''(experimental) Returns a CloudFormation stack artifact from this assembly.

        :param artifact_id: the artifact id of the stack (can be obtained through ``stack.artifactId``).

        :return: a ``CloudFormationStackArtifact`` object.

        :stability: experimental
        :throws: if there is no stack artifact with that id
        '''
        return typing.cast("CloudFormationStackArtifact", jsii.invoke(self, "getStackArtifact", [artifact_id]))

    @jsii.member(jsii_name="getStackByName")
    def get_stack_by_name(
        self,
        stack_name: builtins.str,
    ) -> "CloudFormationStackArtifact":
        '''(experimental) Returns a CloudFormation stack artifact from this assembly.

        Will only search the current assembly.

        :param stack_name: the name of the CloudFormation stack.

        :return: a ``CloudFormationStackArtifact`` object.

        :stability: experimental
        :throws:

        if there is more than one stack with the same stack name. You can
        use ``getStackArtifact(stack.artifactId)`` instead.
        '''
        return typing.cast("CloudFormationStackArtifact", jsii.invoke(self, "getStackByName", [stack_name]))

    @jsii.member(jsii_name="tree")
    def tree(self) -> typing.Optional["TreeCloudArtifact"]:
        '''(experimental) Returns the tree metadata artifact from this assembly.

        :return: a ``TreeCloudArtifact`` object if there is one defined in the manifest, ``undefined`` otherwise.

        :stability: experimental
        :throws: if there is no metadata artifact by that name
        '''
        return typing.cast(typing.Optional["TreeCloudArtifact"], jsii.invoke(self, "tree", []))

    @jsii.member(jsii_name="tryGetArtifact")
    def try_get_artifact(self, id: builtins.str) -> typing.Optional[CloudArtifact]:
        '''(experimental) Attempts to find an artifact with a specific identity.

        :param id: The artifact ID.

        :return: A ``CloudArtifact`` object or ``undefined`` if the artifact does not exist in this assembly.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[CloudArtifact], jsii.invoke(self, "tryGetArtifact", [id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.List[CloudArtifact]:
        '''(experimental) All artifacts included in this assembly.

        :stability: experimental
        '''
        return typing.cast(typing.List[CloudArtifact], jsii.get(self, "artifacts"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directory")
    def directory(self) -> builtins.str:
        '''(experimental) The root directory of the cloud assembly.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "directory"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> _AssemblyManifest_413b9f23:
        '''(experimental) The raw assembly manifest.

        :stability: experimental
        '''
        return typing.cast(_AssemblyManifest_413b9f23, jsii.get(self, "manifest"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nestedAssemblies")
    def nested_assemblies(self) -> typing.List["NestedCloudAssemblyArtifact"]:
        '''(experimental) The nested assembly artifacts in this assembly.

        :stability: experimental
        '''
        return typing.cast(typing.List["NestedCloudAssemblyArtifact"], jsii.get(self, "nestedAssemblies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> _RuntimeInfo_3e9d9574:
        '''(experimental) Runtime information such as module versions used to synthesize this assembly.

        :stability: experimental
        '''
        return typing.cast(_RuntimeInfo_3e9d9574, jsii.get(self, "runtime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["CloudFormationStackArtifact"]:
        '''
        :return: all the CloudFormation stack artifacts that are included in this assembly.

        :stability: experimental
        '''
        return typing.cast(typing.List["CloudFormationStackArtifact"], jsii.get(self, "stacks"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stacksRecursively")
    def stacks_recursively(self) -> typing.List["CloudFormationStackArtifact"]:
        '''(experimental) Returns all the stacks, including the ones in nested assemblies.

        :stability: experimental
        '''
        return typing.cast(typing.List["CloudFormationStackArtifact"], jsii.get(self, "stacksRecursively"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The schema version of the assembly manifest.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class CloudAssemblyBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.CloudAssemblyBuilder",
):
    '''(experimental) Can be used to build a cloud assembly.

    :stability: experimental
    '''

    def __init__(
        self,
        outdir: typing.Optional[builtins.str] = None,
        *,
        asset_outdir: typing.Optional[builtins.str] = None,
        parent_builder: typing.Optional["CloudAssemblyBuilder"] = None,
    ) -> None:
        '''(experimental) Initializes a cloud assembly builder.

        :param outdir: The output directory, uses temporary directory if undefined.
        :param asset_outdir: (experimental) Use the given asset output directory. Default: - Same as the manifest outdir
        :param parent_builder: (experimental) If this builder is for a nested assembly, the parent assembly builder. Default: - This is a root assembly

        :stability: experimental
        '''
        props = CloudAssemblyBuilderProps(
            asset_outdir=asset_outdir, parent_builder=parent_builder
        )

        jsii.create(CloudAssemblyBuilder, self, [outdir, props])

    @jsii.member(jsii_name="addArtifact")
    def add_artifact(
        self,
        id: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''(experimental) Adds an artifact into the cloud assembly.

        :param id: The ID of the artifact.
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        manifest = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "addArtifact", [id, manifest]))

    @jsii.member(jsii_name="addMissing")
    def add_missing(
        self,
        *,
        key: builtins.str,
        props: typing.Union[_AmiContextQuery_74bf4b1b, _AvailabilityZonesContextQuery_715a9fea, _HostedZoneContextQuery_8e6ca28f, _SSMParameterContextQuery_675de122, _VpcContextQuery_a193c650, _EndpointServiceAvailabilityZonesContextQuery_ea3ca0d1, _LoadBalancerContextQuery_cb08d67c, _LoadBalancerListenerContextQuery_0eaf3c16, _SecurityGroupContextQuery_e772f3e6],
        provider: _ContextProvider_fa789bb5,
    ) -> None:
        '''(experimental) Reports that some context is missing in order for this cloud assembly to be fully synthesized.

        :param key: (experimental) The missing context key.
        :param props: (experimental) A set of provider-specific options.
        :param provider: (experimental) The provider from which we expect this context key to be obtained.

        :stability: experimental
        '''
        missing = _MissingContext_0ff9e334(key=key, props=props, provider=provider)

        return typing.cast(None, jsii.invoke(self, "addMissing", [missing]))

    @jsii.member(jsii_name="buildAssembly")
    def build_assembly(self) -> CloudAssembly:
        '''(experimental) Finalizes the cloud assembly into the output directory returns a ``CloudAssembly`` object that can be used to inspect the assembly.

        :stability: experimental
        '''
        options = AssemblyBuildOptions()

        return typing.cast(CloudAssembly, jsii.invoke(self, "buildAssembly", [options]))

    @jsii.member(jsii_name="createNestedAssembly")
    def create_nested_assembly(
        self,
        artifact_id: builtins.str,
        display_name: builtins.str,
    ) -> "CloudAssemblyBuilder":
        '''(experimental) Creates a nested cloud assembly.

        :param artifact_id: -
        :param display_name: -

        :stability: experimental
        '''
        return typing.cast("CloudAssemblyBuilder", jsii.invoke(self, "createNestedAssembly", [artifact_id, display_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assetOutdir")
    def asset_outdir(self) -> builtins.str:
        '''(experimental) The directory where assets of this Cloud Assembly should be stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assetOutdir"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        '''(experimental) The root directory of the resulting cloud assembly.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outdir"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.CloudAssemblyBuilderProps",
    jsii_struct_bases=[],
    name_mapping={"asset_outdir": "assetOutdir", "parent_builder": "parentBuilder"},
)
class CloudAssemblyBuilderProps:
    def __init__(
        self,
        *,
        asset_outdir: typing.Optional[builtins.str] = None,
        parent_builder: typing.Optional[CloudAssemblyBuilder] = None,
    ) -> None:
        '''(experimental) Construction properties for CloudAssemblyBuilder.

        :param asset_outdir: (experimental) Use the given asset output directory. Default: - Same as the manifest outdir
        :param parent_builder: (experimental) If this builder is for a nested assembly, the parent assembly builder. Default: - This is a root assembly

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if asset_outdir is not None:
            self._values["asset_outdir"] = asset_outdir
        if parent_builder is not None:
            self._values["parent_builder"] = parent_builder

    @builtins.property
    def asset_outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the given asset output directory.

        :default: - Same as the manifest outdir

        :stability: experimental
        '''
        result = self._values.get("asset_outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_builder(self) -> typing.Optional[CloudAssemblyBuilder]:
        '''(experimental) If this builder is for a nested assembly, the parent assembly builder.

        :default: - This is a root assembly

        :stability: experimental
        '''
        result = self._values.get("parent_builder")
        return typing.cast(typing.Optional[CloudAssemblyBuilder], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAssemblyBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFormationStackArtifact(
    CloudArtifact,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.CloudFormationStackArtifact",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        assembly: CloudAssembly,
        artifact_id: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''
        :param assembly: -
        :param artifact_id: -
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        artifact = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        jsii.create(CloudFormationStackArtifact, self, [assembly, artifact_id, artifact])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assets")
    def assets(
        self,
    ) -> typing.List[typing.Union[_FileAssetMetadataEntry_50173f8f, _ContainerImageAssetMetadataEntry_0a212d1d]]:
        '''(experimental) Any assets associated with this stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Union[_FileAssetMetadataEntry_50173f8f, _ContainerImageAssetMetadataEntry_0a212d1d]], jsii.get(self, "assets"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''(experimental) A string that represents this stack.

        Should only be used in user interfaces.
        If the stackName and artifactId are the same, it will just return that. Otherwise,
        it will return something like " ()"

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="environment")
    def environment(self) -> "Environment":
        '''(experimental) The environment into which to deploy this artifact.

        :stability: experimental
        '''
        return typing.cast("Environment", jsii.get(self, "environment"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="originalName")
    def original_name(self) -> builtins.str:
        '''(experimental) The original name as defined in the CDK app.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "originalName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) CloudFormation parameters to pass to the stack.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''(experimental) The physical name of this stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) CloudFormation tags to pass to the stack.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="template")
    def template(self) -> typing.Any:
        '''(experimental) The CloudFormation template for this stack.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "template"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateFile")
    def template_file(self) -> builtins.str:
        '''(experimental) The file name of the template.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateFile"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateFullPath")
    def template_full_path(self) -> builtins.str:
        '''(experimental) Full path to the template file.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "templateFullPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assumeRoleArn")
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that needs to be assumed to deploy the stack.

        :default: - No role is assumed (current credentials are used)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assumeRoleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bootstrapStackVersionSsmParameter")
    def bootstrap_stack_version_ssm_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of SSM parameter with bootstrap stack version.

        :default: - Discover SSM parameter by reading stack

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapStackVersionSsmParameter"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cloudFormationExecutionRoleArn")
    def cloud_formation_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that is passed to CloudFormation to execute the change set.

        :default: - No role is passed (currently assumed role/credentials are used)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudFormationExecutionRoleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="requiresBootstrapStackVersion")
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of bootstrap stack required to deploy this stack.

        :default: - No bootstrap stack required

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "requiresBootstrapStackVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackTemplateAssetObjectUrl")
    def stack_template_asset_object_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the stack template has already been included in the asset manifest, its asset URL.

        :default: - Not uploaded yet, upload just before deploying

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackTemplateAssetObjectUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terminationProtection")
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether termination protection is enabled for this stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "terminationProtection"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="validateOnSynth")
    def validate_on_synth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this stack should be validated by the CLI after synthesis.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "validateOnSynth"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.EndpointServiceAvailabilityZonesContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "service_name": "serviceName",
    },
)
class EndpointServiceAvailabilityZonesContextQuery:
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query to hosted zone context provider.

        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param service_name: (experimental) Query service name.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if region is not None:
            self._values["region"] = region
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Query service name.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointServiceAvailabilityZonesContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.Environment",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "name": "name", "region": "region"},
)
class Environment:
    def __init__(
        self,
        *,
        account: builtins.str,
        name: builtins.str,
        region: builtins.str,
    ) -> None:
        '''(experimental) Models an AWS execution environment, for use within the CDK toolkit.

        :param account: (experimental) The AWS account this environment deploys into.
        :param name: (experimental) The arbitrary name of this environment (user-set, or at least user-meaningful).
        :param region: (experimental) The AWS region name where this environment deploys into.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "account": account,
            "name": name,
            "region": region,
        }

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) The AWS account this environment deploys into.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The arbitrary name of this environment (user-set, or at least user-meaningful).

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) The AWS region name where this environment deploys into.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Environment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.EnvironmentPlaceholderValues",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "partition": "partition",
        "region": "region",
    },
)
class EnvironmentPlaceholderValues:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        partition: builtins.str,
        region: builtins.str,
    ) -> None:
        '''(experimental) Return the appropriate values for the environment placeholders.

        :param account_id: (experimental) Return the account.
        :param partition: (experimental) Return the partition.
        :param region: (experimental) Return the region.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "partition": partition,
            "region": region,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''(experimental) Return the account.

        :stability: experimental
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partition(self) -> builtins.str:
        '''(experimental) Return the partition.

        :stability: experimental
        '''
        result = self._values.get("partition")
        assert result is not None, "Required property 'partition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Return the region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentPlaceholderValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvironmentPlaceholders(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.EnvironmentPlaceholders",
):
    '''(experimental) Placeholders which can be used manifests.

    These can occur both in the Asset Manifest as well as the general
    Cloud Assembly manifest.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(EnvironmentPlaceholders, self, [])

    @jsii.member(jsii_name="replace") # type: ignore[misc]
    @builtins.classmethod
    def replace(
        cls,
        object: typing.Any,
        *,
        account_id: builtins.str,
        partition: builtins.str,
        region: builtins.str,
    ) -> typing.Any:
        '''(experimental) Replace the environment placeholders in all strings found in a complex object.

        Duplicated between cdk-assets and aws-cdk CLI because we don't have a good single place to put it
        (they're nominally independent tools).

        :param object: -
        :param account_id: (experimental) Return the account.
        :param partition: (experimental) Return the partition.
        :param region: (experimental) Return the region.

        :stability: experimental
        '''
        values = EnvironmentPlaceholderValues(
            account_id=account_id, partition=partition, region=region
        )

        return typing.cast(typing.Any, jsii.sinvoke(cls, "replace", [object, values]))

    @jsii.member(jsii_name="replaceAsync") # type: ignore[misc]
    @builtins.classmethod
    def replace_async(
        cls,
        object: typing.Any,
        provider: "IEnvironmentPlaceholderProvider",
    ) -> typing.Any:
        '''(experimental) Like 'replace', but asynchronous.

        :param object: -
        :param provider: -

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.sinvoke(cls, "replaceAsync", [object, provider]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CURRENT_ACCOUNT")
    def CURRENT_ACCOUNT(cls) -> builtins.str:
        '''(experimental) Insert this into the destination fields to be replaced with the current account.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CURRENT_ACCOUNT"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CURRENT_PARTITION")
    def CURRENT_PARTITION(cls) -> builtins.str:
        '''(experimental) Insert this into the destination fields to be replaced with the current partition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CURRENT_PARTITION"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CURRENT_REGION")
    def CURRENT_REGION(cls) -> builtins.str:
        '''(experimental) Insert this into the destination fields to be replaced with the current region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CURRENT_REGION"))


class EnvironmentUtils(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.EnvironmentUtils",
):
    '''
    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(EnvironmentUtils, self, [])

    @jsii.member(jsii_name="format") # type: ignore[misc]
    @builtins.classmethod
    def format(cls, account: builtins.str, region: builtins.str) -> builtins.str:
        '''(experimental) Format an environment string from an account and region.

        :param account: -
        :param region: -

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "format", [account, region]))

    @jsii.member(jsii_name="make") # type: ignore[misc]
    @builtins.classmethod
    def make(cls, account: builtins.str, region: builtins.str) -> Environment:
        '''(experimental) Build an environment object from an account and region.

        :param account: -
        :param region: -

        :stability: experimental
        '''
        return typing.cast(Environment, jsii.sinvoke(cls, "make", [account, region]))

    @jsii.member(jsii_name="parse") # type: ignore[misc]
    @builtins.classmethod
    def parse(cls, environment: builtins.str) -> Environment:
        '''
        :param environment: -

        :stability: experimental
        '''
        return typing.cast(Environment, jsii.sinvoke(cls, "parse", [environment]))


@jsii.interface(jsii_type="aws-cdk-lib.cx_api.IEnvironmentPlaceholderProvider")
class IEnvironmentPlaceholderProvider(typing_extensions.Protocol):
    '''(experimental) Return the appropriate values for the environment placeholders.

    :stability: experimental
    '''

    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''(experimental) Return the account.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        '''(experimental) Return the partition.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''(experimental) Return the region.

        :stability: experimental
        '''
        ...


class _IEnvironmentPlaceholderProviderProxy:
    '''(experimental) Return the appropriate values for the environment placeholders.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.cx_api.IEnvironmentPlaceholderProvider"

    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        '''(experimental) Return the account.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "accountId", []))

    @jsii.member(jsii_name="partition")
    def partition(self) -> builtins.str:
        '''(experimental) Return the partition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "partition", []))

    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        '''(experimental) Return the region.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "region", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEnvironmentPlaceholderProvider).__jsii_proxy_class__ = lambda : _IEnvironmentPlaceholderProviderProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.LoadBalancerContextResponse",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address_type": "ipAddressType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_canonical_hosted_zone_id": "loadBalancerCanonicalHostedZoneId",
        "load_balancer_dns_name": "loadBalancerDnsName",
        "security_group_ids": "securityGroupIds",
        "vpc_id": "vpcId",
    },
)
class LoadBalancerContextResponse:
    def __init__(
        self,
        *,
        ip_address_type: "LoadBalancerIpAddressType",
        load_balancer_arn: builtins.str,
        load_balancer_canonical_hosted_zone_id: builtins.str,
        load_balancer_dns_name: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
    ) -> None:
        '''(experimental) Properties of a discovered load balancer.

        :param ip_address_type: (experimental) Type of IP address.
        :param load_balancer_arn: (experimental) The ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: (experimental) The hosted zone ID of the load balancer's name.
        :param load_balancer_dns_name: (experimental) Load balancer's DNS name.
        :param security_group_ids: (experimental) Load balancer's security groups.
        :param vpc_id: (experimental) Load balancer's VPC.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "ip_address_type": ip_address_type,
            "load_balancer_arn": load_balancer_arn,
            "load_balancer_canonical_hosted_zone_id": load_balancer_canonical_hosted_zone_id,
            "load_balancer_dns_name": load_balancer_dns_name,
            "security_group_ids": security_group_ids,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def ip_address_type(self) -> "LoadBalancerIpAddressType":
        '''(experimental) Type of IP address.

        :stability: experimental
        '''
        result = self._values.get("ip_address_type")
        assert result is not None, "Required property 'ip_address_type' is missing"
        return typing.cast("LoadBalancerIpAddressType", result)

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) The ARN of the load balancer.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The hosted zone ID of the load balancer's name.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_canonical_hosted_zone_id")
        assert result is not None, "Required property 'load_balancer_canonical_hosted_zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_dns_name(self) -> builtins.str:
        '''(experimental) Load balancer's DNS name.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_dns_name")
        assert result is not None, "Required property 'load_balancer_dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''(experimental) Load balancer's security groups.

        :stability: experimental
        '''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''(experimental) Load balancer's VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerContextResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.cx_api.LoadBalancerIpAddressType")
class LoadBalancerIpAddressType(enum.Enum):
    '''(experimental) Load balancer ip address type.

    :stability: experimental
    '''

    IPV4 = "IPV4"
    '''(experimental) IPV4 ip address.

    :stability: experimental
    '''
    DUAL_STACK = "DUAL_STACK"
    '''(experimental) Dual stack address.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.LoadBalancerListenerContextResponse",
    jsii_struct_bases=[],
    name_mapping={
        "listener_arn": "listenerArn",
        "listener_port": "listenerPort",
        "security_group_ids": "securityGroupIds",
    },
)
class LoadBalancerListenerContextResponse:
    def __init__(
        self,
        *,
        listener_arn: builtins.str,
        listener_port: jsii.Number,
        security_group_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Properties of a discovered load balancer listener.

        :param listener_arn: (experimental) The ARN of the listener.
        :param listener_port: (experimental) The port the listener is listening on.
        :param security_group_ids: (experimental) The security groups of the load balancer.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener_arn": listener_arn,
            "listener_port": listener_port,
            "security_group_ids": security_group_ids,
        }

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''(experimental) The ARN of the listener.

        :stability: experimental
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listener_port(self) -> jsii.Number:
        '''(experimental) The port the listener is listening on.

        :stability: experimental
        '''
        result = self._values.get("listener_port")
        assert result is not None, "Required property 'listener_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''(experimental) The security groups of the load balancer.

        :stability: experimental
        '''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerListenerContextResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.MetadataEntryResult",
    jsii_struct_bases=[_MetadataEntry_13e1bf79],
    name_mapping={"type": "type", "data": "data", "trace": "trace", "path": "path"},
)
class MetadataEntryResult(_MetadataEntry_13e1bf79):
    def __init__(
        self,
        *,
        type: builtins.str,
        data: typing.Optional[typing.Union[builtins.str, _FileAssetMetadataEntry_50173f8f, _ContainerImageAssetMetadataEntry_0a212d1d, typing.Sequence[_Tag_554dd7f9]]] = None,
        trace: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: builtins.str,
    ) -> None:
        '''
        :param type: (experimental) The type of the metadata entry.
        :param data: (experimental) The data. Default: - no data.
        :param trace: (experimental) A stack trace for when the entry was created. Default: - no trace.
        :param path: (experimental) The path in which this entry was defined.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "type": type,
            "path": path,
        }
        if data is not None:
            self._values["data"] = data
        if trace is not None:
            self._values["trace"] = trace

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The type of the metadata entry.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, _FileAssetMetadataEntry_50173f8f, _ContainerImageAssetMetadataEntry_0a212d1d, typing.List[_Tag_554dd7f9]]]:
        '''(experimental) The data.

        :default: - no data.

        :stability: experimental
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Union[builtins.str, _FileAssetMetadataEntry_50173f8f, _ContainerImageAssetMetadataEntry_0a212d1d, typing.List[_Tag_554dd7f9]]], result)

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A stack trace for when the entry was created.

        :default: - no trace.

        :stability: experimental
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) The path in which this entry was defined.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataEntryResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NestedCloudAssemblyArtifact(
    CloudArtifact,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.NestedCloudAssemblyArtifact",
):
    '''(experimental) Asset manifest is a description of a set of assets which need to be built and published.

    :stability: experimental
    '''

    def __init__(
        self,
        assembly: CloudAssembly,
        name: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''
        :param assembly: -
        :param name: -
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        artifact = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        jsii.create(NestedCloudAssemblyArtifact, self, [assembly, name, artifact])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> builtins.str:
        '''(experimental) The relative directory name of the asset manifest.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "directoryName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''(experimental) Display name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fullPath")
    def full_path(self) -> builtins.str:
        '''(experimental) Full path to the nested assembly directory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "fullPath"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nestedAssembly")
    def nested_assembly(self) -> CloudAssembly:
        '''(experimental) The nested Assembly.

        :stability: experimental
        '''
        return typing.cast(CloudAssembly, jsii.get(self, "nestedAssembly"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.SecurityGroupContextResponse",
    jsii_struct_bases=[],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "security_group_id": "securityGroupId",
    },
)
class SecurityGroupContextResponse:
    def __init__(
        self,
        *,
        allow_all_outbound: builtins.bool,
        security_group_id: builtins.str,
    ) -> None:
        '''(experimental) Properties of a discovered SecurityGroup.

        :param allow_all_outbound: (experimental) Whether the security group allows all outbound traffic. This will be true when the security group has all-protocol egress permissions to access both ``0.0.0.0/0`` and ``::/0``.
        :param security_group_id: (experimental) The security group's id.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "allow_all_outbound": allow_all_outbound,
            "security_group_id": security_group_id,
        }

    @builtins.property
    def allow_all_outbound(self) -> builtins.bool:
        '''(experimental) Whether the security group allows all outbound traffic.

        This will be true
        when the security group has all-protocol egress permissions to access both
        ``0.0.0.0/0`` and ``::/0``.

        :stability: experimental
        '''
        result = self._values.get("allow_all_outbound")
        assert result is not None, "Required property 'allow_all_outbound' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''(experimental) The security group's id.

        :stability: experimental
        '''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupContextResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.SynthesisMessage",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry", "id": "id", "level": "level"},
)
class SynthesisMessage:
    def __init__(
        self,
        *,
        entry: _MetadataEntry_13e1bf79,
        id: builtins.str,
        level: "SynthesisMessageLevel",
    ) -> None:
        '''
        :param entry: 
        :param id: 
        :param level: 

        :stability: experimental
        '''
        if isinstance(entry, dict):
            entry = _MetadataEntry_13e1bf79(**entry)
        self._values: typing.Dict[str, typing.Any] = {
            "entry": entry,
            "id": id,
            "level": level,
        }

    @builtins.property
    def entry(self) -> _MetadataEntry_13e1bf79:
        '''
        :stability: experimental
        '''
        result = self._values.get("entry")
        assert result is not None, "Required property 'entry' is missing"
        return typing.cast(_MetadataEntry_13e1bf79, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def level(self) -> "SynthesisMessageLevel":
        '''
        :stability: experimental
        '''
        result = self._values.get("level")
        assert result is not None, "Required property 'level' is missing"
        return typing.cast("SynthesisMessageLevel", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynthesisMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.cx_api.SynthesisMessageLevel")
class SynthesisMessageLevel(enum.Enum):
    '''
    :stability: experimental
    '''

    INFO = "INFO"
    '''
    :stability: experimental
    '''
    WARNING = "WARNING"
    '''
    :stability: experimental
    '''
    ERROR = "ERROR"
    '''
    :stability: experimental
    '''


class TreeCloudArtifact(
    CloudArtifact,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.TreeCloudArtifact",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        assembly: CloudAssembly,
        name: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''
        :param assembly: -
        :param name: -
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        artifact = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        jsii.create(TreeCloudArtifact, self, [assembly, name, artifact])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "file"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.VpcContextResponse",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "vpc_id": "vpcId",
        "isolated_subnet_ids": "isolatedSubnetIds",
        "isolated_subnet_names": "isolatedSubnetNames",
        "isolated_subnet_route_table_ids": "isolatedSubnetRouteTableIds",
        "private_subnet_ids": "privateSubnetIds",
        "private_subnet_names": "privateSubnetNames",
        "private_subnet_route_table_ids": "privateSubnetRouteTableIds",
        "public_subnet_ids": "publicSubnetIds",
        "public_subnet_names": "publicSubnetNames",
        "public_subnet_route_table_ids": "publicSubnetRouteTableIds",
        "subnet_groups": "subnetGroups",
        "vpc_cidr_block": "vpcCidrBlock",
        "vpn_gateway_id": "vpnGatewayId",
    },
)
class VpcContextResponse:
    def __init__(
        self,
        *,
        availability_zones: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        isolated_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        isolated_subnet_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        isolated_subnet_route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_subnet_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_subnet_route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        public_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        public_subnet_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        public_subnet_route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_groups: typing.Optional[typing.Sequence["VpcSubnetGroup"]] = None,
        vpc_cidr_block: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of a discovered VPC.

        :param availability_zones: (experimental) AZs.
        :param vpc_id: (experimental) VPC id.
        :param isolated_subnet_ids: (experimental) IDs of all isolated subnets. Element count: #(availabilityZones) · #(isolatedGroups)
        :param isolated_subnet_names: (experimental) Name of isolated subnet groups. Element count: #(isolatedGroups)
        :param isolated_subnet_route_table_ids: (experimental) Route Table IDs of isolated subnet groups. Element count: #(availabilityZones) · #(isolatedGroups)
        :param private_subnet_ids: (experimental) IDs of all private subnets. Element count: #(availabilityZones) · #(privateGroups)
        :param private_subnet_names: (experimental) Name of private subnet groups. Element count: #(privateGroups)
        :param private_subnet_route_table_ids: (experimental) Route Table IDs of private subnet groups. Element count: #(availabilityZones) · #(privateGroups)
        :param public_subnet_ids: (experimental) IDs of all public subnets. Element count: #(availabilityZones) · #(publicGroups)
        :param public_subnet_names: (experimental) Name of public subnet groups. Element count: #(publicGroups)
        :param public_subnet_route_table_ids: (experimental) Route Table IDs of public subnet groups. Element count: #(availabilityZones) · #(publicGroups)
        :param subnet_groups: (experimental) The subnet groups discovered for the given VPC. Unlike the above properties, this will include asymmetric subnets, if the VPC has any. This property will only be populated if {@link VpcContextQuery.returnAsymmetricSubnets} is true. Default: - no subnet groups will be returned unless {@link VpcContextQuery.returnAsymmetricSubnets} is true
        :param vpc_cidr_block: (experimental) VPC cidr. Default: - CIDR information not available
        :param vpn_gateway_id: (experimental) The VPN gateway ID.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zones": availability_zones,
            "vpc_id": vpc_id,
        }
        if isolated_subnet_ids is not None:
            self._values["isolated_subnet_ids"] = isolated_subnet_ids
        if isolated_subnet_names is not None:
            self._values["isolated_subnet_names"] = isolated_subnet_names
        if isolated_subnet_route_table_ids is not None:
            self._values["isolated_subnet_route_table_ids"] = isolated_subnet_route_table_ids
        if private_subnet_ids is not None:
            self._values["private_subnet_ids"] = private_subnet_ids
        if private_subnet_names is not None:
            self._values["private_subnet_names"] = private_subnet_names
        if private_subnet_route_table_ids is not None:
            self._values["private_subnet_route_table_ids"] = private_subnet_route_table_ids
        if public_subnet_ids is not None:
            self._values["public_subnet_ids"] = public_subnet_ids
        if public_subnet_names is not None:
            self._values["public_subnet_names"] = public_subnet_names
        if public_subnet_route_table_ids is not None:
            self._values["public_subnet_route_table_ids"] = public_subnet_route_table_ids
        if subnet_groups is not None:
            self._values["subnet_groups"] = subnet_groups
        if vpc_cidr_block is not None:
            self._values["vpc_cidr_block"] = vpc_cidr_block
        if vpn_gateway_id is not None:
            self._values["vpn_gateway_id"] = vpn_gateway_id

    @builtins.property
    def availability_zones(self) -> typing.List[builtins.str]:
        '''(experimental) AZs.

        :stability: experimental
        '''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''(experimental) VPC id.

        :stability: experimental
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def isolated_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) IDs of all isolated subnets.

        Element count: #(availabilityZones) · #(isolatedGroups)

        :stability: experimental
        '''
        result = self._values.get("isolated_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def isolated_subnet_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Name of isolated subnet groups.

        Element count: #(isolatedGroups)

        :stability: experimental
        '''
        result = self._values.get("isolated_subnet_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def isolated_subnet_route_table_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Route Table IDs of isolated subnet groups.

        Element count: #(availabilityZones) · #(isolatedGroups)

        :stability: experimental
        '''
        result = self._values.get("isolated_subnet_route_table_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) IDs of all private subnets.

        Element count: #(availabilityZones) · #(privateGroups)

        :stability: experimental
        '''
        result = self._values.get("private_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_subnet_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Name of private subnet groups.

        Element count: #(privateGroups)

        :stability: experimental
        '''
        result = self._values.get("private_subnet_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_subnet_route_table_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Route Table IDs of private subnet groups.

        Element count: #(availabilityZones) · #(privateGroups)

        :stability: experimental
        '''
        result = self._values.get("private_subnet_route_table_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def public_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) IDs of all public subnets.

        Element count: #(availabilityZones) · #(publicGroups)

        :stability: experimental
        '''
        result = self._values.get("public_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def public_subnet_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Name of public subnet groups.

        Element count: #(publicGroups)

        :stability: experimental
        '''
        result = self._values.get("public_subnet_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def public_subnet_route_table_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Route Table IDs of public subnet groups.

        Element count: #(availabilityZones) · #(publicGroups)

        :stability: experimental
        '''
        result = self._values.get("public_subnet_route_table_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_groups(self) -> typing.Optional[typing.List["VpcSubnetGroup"]]:
        '''(experimental) The subnet groups discovered for the given VPC.

        Unlike the above properties, this will include asymmetric subnets,
        if the VPC has any.
        This property will only be populated if {@link VpcContextQuery.returnAsymmetricSubnets}
        is true.

        :default: - no subnet groups will be returned unless {@link VpcContextQuery.returnAsymmetricSubnets} is true

        :stability: experimental
        '''
        result = self._values.get("subnet_groups")
        return typing.cast(typing.Optional[typing.List["VpcSubnetGroup"]], result)

    @builtins.property
    def vpc_cidr_block(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC cidr.

        :default: - CIDR information not available

        :stability: experimental
        '''
        result = self._values.get("vpc_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_gateway_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The VPN gateway ID.

        :stability: experimental
        '''
        result = self._values.get("vpn_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcContextResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.VpcSubnet",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "route_table_id": "routeTableId",
        "subnet_id": "subnetId",
        "cidr": "cidr",
    },
)
class VpcSubnet:
    def __init__(
        self,
        *,
        availability_zone: builtins.str,
        route_table_id: builtins.str,
        subnet_id: builtins.str,
        cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A subnet representation that the VPC provider uses.

        :param availability_zone: (experimental) The code of the availability zone this subnet is in (for example, 'us-west-2a').
        :param route_table_id: (experimental) The identifier of the route table for this subnet.
        :param subnet_id: (experimental) The identifier of the subnet.
        :param cidr: (experimental) CIDR range of the subnet. Default: - CIDR information not available

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zone": availability_zone,
            "route_table_id": route_table_id,
            "subnet_id": subnet_id,
        }
        if cidr is not None:
            self._values["cidr"] = cidr

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''(experimental) The code of the availability zone this subnet is in (for example, 'us-west-2a').

        :stability: experimental
        '''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_table_id(self) -> builtins.str:
        '''(experimental) The identifier of the route table for this subnet.

        :stability: experimental
        '''
        result = self._values.get("route_table_id")
        assert result is not None, "Required property 'route_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''(experimental) The identifier of the subnet.

        :stability: experimental
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        '''(experimental) CIDR range of the subnet.

        :default: - CIDR information not available

        :stability: experimental
        '''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcSubnet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.cx_api.VpcSubnetGroup",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "subnets": "subnets", "type": "type"},
)
class VpcSubnetGroup:
    def __init__(
        self,
        *,
        name: builtins.str,
        subnets: typing.Sequence[VpcSubnet],
        type: "VpcSubnetGroupType",
    ) -> None:
        '''(experimental) A group of subnets returned by the VPC provider.

        The included subnets do NOT have to be symmetric!

        :param name: (experimental) The name of the subnet group, determined by looking at the tags of of the subnets that belong to it.
        :param subnets: (experimental) The subnets that are part of this group. There is no condition that the subnets have to be symmetric in the group.
        :param type: (experimental) The type of the subnet group.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "subnets": subnets,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the subnet group, determined by looking at the tags of of the subnets that belong to it.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnets(self) -> typing.List[VpcSubnet]:
        '''(experimental) The subnets that are part of this group.

        There is no condition that the subnets have to be symmetric
        in the group.

        :stability: experimental
        '''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[VpcSubnet], result)

    @builtins.property
    def type(self) -> "VpcSubnetGroupType":
        '''(experimental) The type of the subnet group.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("VpcSubnetGroupType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcSubnetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.cx_api.VpcSubnetGroupType")
class VpcSubnetGroupType(enum.Enum):
    '''(experimental) The type of subnet group.

    Same as SubnetType in the @aws-cdk/aws-ec2 package,
    but we can't use that because of cyclical dependencies.

    :stability: experimental
    '''

    PUBLIC = "PUBLIC"
    '''(experimental) Public subnet group type.

    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''(experimental) Private subnet group type.

    :stability: experimental
    '''
    ISOLATED = "ISOLATED"
    '''(experimental) Isolated subnet group type.

    :stability: experimental
    '''


class AssetManifestArtifact(
    CloudArtifact,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.cx_api.AssetManifestArtifact",
):
    '''(experimental) Asset manifest is a description of a set of assets which need to be built and published.

    :stability: experimental
    '''

    def __init__(
        self,
        assembly: CloudAssembly,
        name: builtins.str,
        *,
        type: _ArtifactType_1d870526,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[_MetadataEntry_13e1bf79]]] = None,
        properties: typing.Optional[typing.Union[_AwsCloudFormationStackProperties_50fb16af, _AssetManifestProperties_9084879a, _TreeArtifactProperties_4092757e, _NestedCloudAssemblyProperties_c2fa342d]] = None,
    ) -> None:
        '''
        :param assembly: -
        :param name: -
        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        '''
        artifact = _ArtifactManifest_f79eef21(
            type=type,
            dependencies=dependencies,
            display_name=display_name,
            environment=environment,
            metadata=metadata,
            properties=properties,
        )

        jsii.create(AssetManifestArtifact, self, [assembly, name, artifact])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        '''(experimental) The file name of the asset manifest.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="requiresBootstrapStackVersion")
    def requires_bootstrap_stack_version(self) -> jsii.Number:
        '''(experimental) Version of bootstrap stack required to deploy this stack.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "requiresBootstrapStackVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bootstrapStackVersionSsmParameter")
    def bootstrap_stack_version_ssm_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of SSM parameter with bootstrap stack version.

        :default: - Discover SSM parameter by reading stack

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bootstrapStackVersionSsmParameter"))


__all__ = [
    "AssemblyBuildOptions",
    "AssetManifestArtifact",
    "AwsCloudFormationStackProperties",
    "CloudArtifact",
    "CloudAssembly",
    "CloudAssemblyBuilder",
    "CloudAssemblyBuilderProps",
    "CloudFormationStackArtifact",
    "EndpointServiceAvailabilityZonesContextQuery",
    "Environment",
    "EnvironmentPlaceholderValues",
    "EnvironmentPlaceholders",
    "EnvironmentUtils",
    "IEnvironmentPlaceholderProvider",
    "LoadBalancerContextResponse",
    "LoadBalancerIpAddressType",
    "LoadBalancerListenerContextResponse",
    "MetadataEntryResult",
    "NestedCloudAssemblyArtifact",
    "SecurityGroupContextResponse",
    "SynthesisMessage",
    "SynthesisMessageLevel",
    "TreeCloudArtifact",
    "VpcContextResponse",
    "VpcSubnet",
    "VpcSubnetGroup",
    "VpcSubnetGroupType",
]

publication.publish()

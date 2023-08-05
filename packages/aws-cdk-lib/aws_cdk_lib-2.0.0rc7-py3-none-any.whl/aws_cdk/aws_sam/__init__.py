import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_9df397a6,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnApi(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnApi",
):
    '''A CloudFormation ``AWS::Serverless::Api``.

    :cloudformationResource: AWS::Serverless::Api
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_da3f097b]] = None,
        auth: typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_da3f097b]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_da3f097b]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_da3f097b]] = None,
        endpoint_configuration: typing.Optional[builtins.str] = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        variables: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.
        '''
        props = CfnApiProps(
            stage_name=stage_name,
            access_log_setting=access_log_setting,
            auth=auth,
            binary_media_types=binary_media_types,
            cache_cluster_enabled=cache_cluster_enabled,
            cache_cluster_size=cache_cluster_size,
            cors=cors,
            definition_body=definition_body,
            definition_uri=definition_uri,
            endpoint_configuration=endpoint_configuration,
            method_settings=method_settings,
            name=name,
            open_api_version=open_api_version,
            tracing_enabled=tracing_enabled,
            variables=variables,
        )

        jsii.create(CfnApi, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Any, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: typing.Any) -> None:
        jsii.set(self, "definitionBody", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))

    @stage_name.setter
    def stage_name(self, value: builtins.str) -> None:
        jsii.set(self, "stageName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessLogSetting")
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_da3f097b]], jsii.get(self, "accessLogSetting"))

    @access_log_setting.setter
    def access_log_setting(
        self,
        value: typing.Optional[typing.Union["CfnApi.AccessLogSettingProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "accessLogSetting", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_da3f097b]], jsii.get(self, "auth"))

    @auth.setter
    def auth(
        self,
        value: typing.Optional[typing.Union["CfnApi.AuthProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "auth", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="binaryMediaTypes")
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "binaryMediaTypes"))

    @binary_media_types.setter
    def binary_media_types(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "binaryMediaTypes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cacheClusterEnabled")
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "cacheClusterEnabled"))

    @cache_cluster_enabled.setter
    def cache_cluster_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "cacheClusterEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cacheClusterSize")
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheClusterSize"))

    @cache_cluster_size.setter
    def cache_cluster_size(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheClusterSize", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cors")
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "cors"))

    @cors.setter
    def cors(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnApi.CorsConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "cors", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_da3f097b]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnApi.S3LocationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "definitionUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointConfiguration")
    def endpoint_configuration(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointConfiguration"))

    @endpoint_configuration.setter
    def endpoint_configuration(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endpointConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="methodSettings")
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]], jsii.get(self, "methodSettings"))

    @method_settings.setter
    def method_settings(
        self,
        value: typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "methodSettings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="openApiVersion")
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "openApiVersion"))

    @open_api_version.setter
    def open_api_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "openApiVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tracingEnabled")
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "tracingEnabled"))

    @tracing_enabled.setter
    def tracing_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "tracingEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "variables"))

    @variables.setter
    def variables(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "variables", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnApi.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: ``CfnApi.AccessLogSettingProperty.DestinationArn``.
            :param format: ``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.DestinationArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AccessLogSettingProperty.Format``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnApi.AuthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizers": "authorizers",
            "default_authorizer": "defaultAuthorizer",
        },
    )
    class AuthProperty:
        def __init__(
            self,
            *,
            authorizers: typing.Any = None,
            default_authorizer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorizers: ``CfnApi.AuthProperty.Authorizers``.
            :param default_authorizer: ``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if authorizers is not None:
                self._values["authorizers"] = authorizers
            if default_authorizer is not None:
                self._values["default_authorizer"] = default_authorizer

        @builtins.property
        def authorizers(self) -> typing.Any:
            '''``CfnApi.AuthProperty.Authorizers``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("authorizers")
            return typing.cast(typing.Any, result)

        @builtins.property
        def default_authorizer(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.AuthProperty.DefaultAuthorizer``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api-auth-object
            '''
            result = self._values.get("default_authorizer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnApi.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_origin": "allowOrigin",
            "allow_credentials": "allowCredentials",
            "allow_headers": "allowHeaders",
            "allow_methods": "allowMethods",
            "max_age": "maxAge",
        },
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            allow_origin: builtins.str,
            allow_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            allow_headers: typing.Optional[builtins.str] = None,
            allow_methods: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allow_origin: ``CfnApi.CorsConfigurationProperty.AllowOrigin``.
            :param allow_credentials: ``CfnApi.CorsConfigurationProperty.AllowCredentials``.
            :param allow_headers: ``CfnApi.CorsConfigurationProperty.AllowHeaders``.
            :param allow_methods: ``CfnApi.CorsConfigurationProperty.AllowMethods``.
            :param max_age: ``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "allow_origin": allow_origin,
            }
            if allow_credentials is not None:
                self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None:
                self._values["allow_headers"] = allow_headers
            if allow_methods is not None:
                self._values["allow_methods"] = allow_methods
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allow_origin(self) -> builtins.str:
            '''``CfnApi.CorsConfigurationProperty.AllowOrigin``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_origin")
            assert result is not None, "Required property 'allow_origin' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allow_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnApi.CorsConfigurationProperty.AllowCredentials``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def allow_headers(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowHeaders``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_headers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def allow_methods(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.AllowMethods``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("allow_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[builtins.str]:
            '''``CfnApi.CorsConfigurationProperty.MaxAge``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cors-configuration
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnApi.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: jsii.Number,
        ) -> None:
            '''
            :param bucket: ``CfnApi.S3LocationProperty.Bucket``.
            :param key: ``CfnApi.S3LocationProperty.Key``.
            :param version: ``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "version": version,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnApi.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> jsii.Number:
            '''``CfnApi.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "stage_name": "stageName",
        "access_log_setting": "accessLogSetting",
        "auth": "auth",
        "binary_media_types": "binaryMediaTypes",
        "cache_cluster_enabled": "cacheClusterEnabled",
        "cache_cluster_size": "cacheClusterSize",
        "cors": "cors",
        "definition_body": "definitionBody",
        "definition_uri": "definitionUri",
        "endpoint_configuration": "endpointConfiguration",
        "method_settings": "methodSettings",
        "name": "name",
        "open_api_version": "openApiVersion",
        "tracing_enabled": "tracingEnabled",
        "variables": "variables",
    },
)
class CfnApiProps:
    def __init__(
        self,
        *,
        stage_name: builtins.str,
        access_log_setting: typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_da3f097b]] = None,
        auth: typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_da3f097b]] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_da3f097b]] = None,
        definition_body: typing.Any = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_da3f097b]] = None,
        endpoint_configuration: typing.Optional[builtins.str] = None,
        method_settings: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        open_api_version: typing.Optional[builtins.str] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        variables: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::Api``.

        :param stage_name: ``AWS::Serverless::Api.StageName``.
        :param access_log_setting: ``AWS::Serverless::Api.AccessLogSetting``.
        :param auth: ``AWS::Serverless::Api.Auth``.
        :param binary_media_types: ``AWS::Serverless::Api.BinaryMediaTypes``.
        :param cache_cluster_enabled: ``AWS::Serverless::Api.CacheClusterEnabled``.
        :param cache_cluster_size: ``AWS::Serverless::Api.CacheClusterSize``.
        :param cors: ``AWS::Serverless::Api.Cors``.
        :param definition_body: ``AWS::Serverless::Api.DefinitionBody``.
        :param definition_uri: ``AWS::Serverless::Api.DefinitionUri``.
        :param endpoint_configuration: ``AWS::Serverless::Api.EndpointConfiguration``.
        :param method_settings: ``AWS::Serverless::Api.MethodSettings``.
        :param name: ``AWS::Serverless::Api.Name``.
        :param open_api_version: ``AWS::Serverless::Api.OpenApiVersion``.
        :param tracing_enabled: ``AWS::Serverless::Api.TracingEnabled``.
        :param variables: ``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "stage_name": stage_name,
        }
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if auth is not None:
            self._values["auth"] = auth
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if cache_cluster_enabled is not None:
            self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None:
            self._values["cache_cluster_size"] = cache_cluster_size
        if cors is not None:
            self._values["cors"] = cors
        if definition_body is not None:
            self._values["definition_body"] = definition_body
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if method_settings is not None:
            self._values["method_settings"] = method_settings
        if name is not None:
            self._values["name"] = name
        if open_api_version is not None:
            self._values["open_api_version"] = open_api_version
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''``AWS::Serverless::Api.StageName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.AccessLogSetting``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[CfnApi.AccessLogSettingProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def auth(
        self,
    ) -> typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.Auth``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[typing.Union[CfnApi.AuthProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Api.BinaryMediaTypes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.CacheClusterEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.CacheClusterSize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cache_cluster_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.Cors``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnApi.CorsConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def definition_body(self) -> typing.Any:
        '''``AWS::Serverless::Api.DefinitionBody``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.DefinitionUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnApi.S3LocationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def endpoint_configuration(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.EndpointConfiguration``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.MethodSettings``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("method_settings")
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.Name``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_api_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Api.OpenApiVersion``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("open_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Api.TracingEnabled``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Api.Variables``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapi
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnApplication(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnApplication",
):
    '''A CloudFormation ``AWS::Serverless::Application``.

    :cloudformationResource: AWS::Serverless::Application
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        location: typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_da3f097b],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.
        '''
        props = CfnApplicationProps(
            location=location,
            notification_arns=notification_arns,
            parameters=parameters,
            tags=tags,
            timeout_in_minutes=timeout_in_minutes,
        )

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_da3f097b]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_da3f097b], jsii.get(self, "location"))

    @location.setter
    def location(
        self,
        value: typing.Union[builtins.str, "CfnApplication.ApplicationLocationProperty", _IResolvable_da3f097b],
    ) -> None:
        jsii.set(self, "location", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationArns")
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationArns"))

    @notification_arns.setter
    def notification_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "notificationArns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMinutes", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnApplication.ApplicationLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_id": "applicationId",
            "semantic_version": "semanticVersion",
        },
    )
    class ApplicationLocationProperty:
        def __init__(
            self,
            *,
            application_id: builtins.str,
            semantic_version: builtins.str,
        ) -> None:
            '''
            :param application_id: ``CfnApplication.ApplicationLocationProperty.ApplicationId``.
            :param semantic_version: ``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "application_id": application_id,
                "semantic_version": semantic_version,
            }

        @builtins.property
        def application_id(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.ApplicationId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("application_id")
            assert result is not None, "Required property 'application_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def semantic_version(self) -> builtins.str:
            '''``CfnApplication.ApplicationLocationProperty.SemanticVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
            '''
            result = self._values.get("semantic_version")
            assert result is not None, "Required property 'semantic_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        location: typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_da3f097b],
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::Application``.

        :param location: ``AWS::Serverless::Application.Location``.
        :param notification_arns: ``AWS::Serverless::Application.NotificationArns``.
        :param parameters: ``AWS::Serverless::Application.Parameters``.
        :param tags: ``AWS::Serverless::Application.Tags``.
        :param timeout_in_minutes: ``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "location": location,
        }
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def location(
        self,
    ) -> typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_da3f097b]:
        '''``AWS::Serverless::Application.Location``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(typing.Union[builtins.str, CfnApplication.ApplicationLocationProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Application.NotificationArns``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::Application.Parameters``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Application.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Application.TimeoutInMinutes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessapplication
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnFunction(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnFunction",
):
    '''A CloudFormation ``AWS::Serverless::Function``.

    :cloudformationResource: AWS::Serverless::Function
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        code_uri: typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_da3f097b],
        handler: builtins.str,
        runtime: builtins.str,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        dead_letter_queue: typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_da3f097b]] = None,
        deployment_preference: typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_da3f097b]] = None,
        events: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_da3f097b]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_da3f097b]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.Sequence[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_da3f097b]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::Function``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.
        '''
        props = CfnFunctionProps(
            code_uri=code_uri,
            handler=handler,
            runtime=runtime,
            auto_publish_alias=auto_publish_alias,
            dead_letter_queue=dead_letter_queue,
            deployment_preference=deployment_preference,
            description=description,
            environment=environment,
            events=events,
            file_system_configs=file_system_configs,
            function_name=function_name,
            kms_key_arn=kms_key_arn,
            layers=layers,
            memory_size=memory_size,
            permissions_boundary=permissions_boundary,
            policies=policies,
            provisioned_concurrency_config=provisioned_concurrency_config,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            tags=tags,
            timeout=timeout,
            tracing=tracing,
            vpc_config=vpc_config,
        )

        jsii.create(CfnFunction, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="codeUri")
    def code_uri(
        self,
    ) -> typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_da3f097b]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_da3f097b], jsii.get(self, "codeUri"))

    @code_uri.setter
    def code_uri(
        self,
        value: typing.Union[builtins.str, "CfnFunction.S3LocationProperty", _IResolvable_da3f097b],
    ) -> None:
        jsii.set(self, "codeUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        jsii.set(self, "handler", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        jsii.set(self, "runtime", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoPublishAlias")
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPublishAlias"))

    @auto_publish_alias.setter
    def auto_publish_alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "autoPublishAlias", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_da3f097b]], jsii.get(self, "deadLetterQueue"))

    @dead_letter_queue.setter
    def dead_letter_queue(
        self,
        value: typing.Optional[typing.Union["CfnFunction.DeadLetterQueueProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "deadLetterQueue", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentPreference")
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_da3f097b]], jsii.get(self, "deploymentPreference"))

    @deployment_preference.setter
    def deployment_preference(
        self,
        value: typing.Optional[typing.Union["CfnFunction.DeploymentPreferenceProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "deploymentPreference", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_da3f097b]], jsii.get(self, "environment"))

    @environment.setter
    def environment(
        self,
        value: typing.Optional[typing.Union["CfnFunction.FunctionEnvironmentProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "environment", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_da3f097b]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnFunction.EventSourceProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "events", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileSystemConfigs")
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_da3f097b]]]], jsii.get(self, "fileSystemConfigs"))

    @file_system_configs.setter
    def file_system_configs(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnFunction.FileSystemConfigProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "fileSystemConfigs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="layers")
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "layers"))

    @layers.setter
    def layers(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "layers", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySize"))

    @memory_size.setter
    def memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "memorySize", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnFunction.IAMPolicyDocumentProperty", "CfnFunction.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "policies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "provisionedConcurrencyConfig"))

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.ProvisionedConcurrencyConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "provisionedConcurrencyConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "reservedConcurrentExecutions"))

    @reserved_concurrent_executions.setter
    def reserved_concurrent_executions(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "reservedConcurrentExecutions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "role", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeout", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tracing")
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tracing"))

    @tracing.setter
    def tracing(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tracing", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.AlexaSkillEventProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class AlexaSkillEventProperty:
        def __init__(
            self,
            *,
            variables: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''
            :param variables: ``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnFunction.AlexaSkillEventProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#alexaskill
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlexaSkillEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={"method": "method", "path": "path", "rest_api_id": "restApiId"},
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnFunction.ApiEventProperty.Method``.
            :param path: ``CfnFunction.ApiEventProperty.Path``.
            :param rest_api_id: ``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnFunction.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.BucketSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class BucketSAMPTProperty:
        def __init__(self, *, bucket_name: builtins.str) -> None:
            '''
            :param bucket_name: ``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFunction.BucketSAMPTProperty.BucketName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.CloudWatchEventEventProperty.Pattern``.
            :param input: ``CfnFunction.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
            }
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.CloudWatchEventEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.CloudWatchLogsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filter_pattern": "filterPattern",
            "log_group_name": "logGroupName",
        },
    )
    class CloudWatchLogsEventProperty:
        def __init__(
            self,
            *,
            filter_pattern: builtins.str,
            log_group_name: builtins.str,
        ) -> None:
            '''
            :param filter_pattern: ``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.
            :param log_group_name: ``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchevent
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "filter_pattern": filter_pattern,
                "log_group_name": log_group_name,
            }

        @builtins.property
        def filter_pattern(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.FilterPattern``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("filter_pattern")
            assert result is not None, "Required property 'filter_pattern' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.CloudWatchLogsEventProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#cloudwatchlogs
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.CollectionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"collection_id": "collectionId"},
    )
    class CollectionSAMPTProperty:
        def __init__(self, *, collection_id: builtins.str) -> None:
            '''
            :param collection_id: ``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "collection_id": collection_id,
            }

        @builtins.property
        def collection_id(self) -> builtins.str:
            '''``CfnFunction.CollectionSAMPTProperty.CollectionId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("collection_id")
            assert result is not None, "Required property 'collection_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CollectionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.DeadLetterQueueProperty",
        jsii_struct_bases=[],
        name_mapping={"target_arn": "targetArn", "type": "type"},
    )
    class DeadLetterQueueProperty:
        def __init__(self, *, target_arn: builtins.str, type: builtins.str) -> None:
            '''
            :param target_arn: ``CfnFunction.DeadLetterQueueProperty.TargetArn``.
            :param type: ``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deadletterqueue-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "target_arn": target_arn,
                "type": type,
            }

        @builtins.property
        def target_arn(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.TargetArn``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("target_arn")
            assert result is not None, "Required property 'target_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeadLetterQueueProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterQueueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.DeploymentPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "type": "type",
            "alarms": "alarms",
            "hooks": "hooks",
        },
    )
    class DeploymentPreferenceProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_da3f097b],
            type: builtins.str,
            alarms: typing.Optional[typing.Sequence[builtins.str]] = None,
            hooks: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnFunction.DeploymentPreferenceProperty.Enabled``.
            :param type: ``CfnFunction.DeploymentPreferenceProperty.Type``.
            :param alarms: ``CfnFunction.DeploymentPreferenceProperty.Alarms``.
            :param hooks: ``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/safe_lambda_deployments.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
                "type": type,
            }
            if alarms is not None:
                self._values["alarms"] = alarms
            if hooks is not None:
                self._values["hooks"] = hooks

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_da3f097b]:
            '''``CfnFunction.DeploymentPreferenceProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_da3f097b], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.DeploymentPreferenceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def alarms(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Alarms``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def hooks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFunction.DeploymentPreferenceProperty.Hooks``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
            '''
            result = self._values.get("hooks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.DestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"on_failure": "onFailure"},
    )
    class DestinationConfigProperty:
        def __init__(
            self,
            *,
            on_failure: typing.Union["CfnFunction.OnFailureProperty", _IResolvable_da3f097b],
        ) -> None:
            '''
            :param on_failure: ``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "on_failure": on_failure,
            }

        @builtins.property
        def on_failure(
            self,
        ) -> typing.Union["CfnFunction.OnFailureProperty", _IResolvable_da3f097b]:
            '''``CfnFunction.DestinationConfigProperty.OnFailure``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("on_failure")
            assert result is not None, "Required property 'on_failure' is missing"
            return typing.cast(typing.Union["CfnFunction.OnFailureProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.DomainSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName"},
    )
    class DomainSAMPTProperty:
        def __init__(self, *, domain_name: builtins.str) -> None:
            '''
            :param domain_name: ``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "domain_name": domain_name,
            }

        @builtins.property
        def domain_name(self) -> builtins.str:
            '''``CfnFunction.DomainSAMPTProperty.DomainName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("domain_name")
            assert result is not None, "Required property 'domain_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.DynamoDBEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "bisect_batch_on_function_error": "bisectBatchOnFunctionError",
            "destination_config": "destinationConfig",
            "enabled": "enabled",
            "maximum_batching_window_in_seconds": "maximumBatchingWindowInSeconds",
            "maximum_record_age_in_seconds": "maximumRecordAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
            "parallelization_factor": "parallelizationFactor",
        },
    )
    class DynamoDBEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            bisect_batch_on_function_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            destination_config: typing.Optional[typing.Union["CfnFunction.DestinationConfigProperty", _IResolvable_da3f097b]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            maximum_batching_window_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_record_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
            parallelization_factor: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.DynamoDBEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.DynamoDBEventProperty.Stream``.
            :param batch_size: ``CfnFunction.DynamoDBEventProperty.BatchSize``.
            :param bisect_batch_on_function_error: ``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.
            :param destination_config: ``CfnFunction.DynamoDBEventProperty.DestinationConfig``.
            :param enabled: ``CfnFunction.DynamoDBEventProperty.Enabled``.
            :param maximum_batching_window_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.
            :param maximum_record_age_in_seconds: ``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.
            :param maximum_retry_attempts: ``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.
            :param parallelization_factor: ``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if bisect_batch_on_function_error is not None:
                self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
            if destination_config is not None:
                self._values["destination_config"] = destination_config
            if enabled is not None:
                self._values["enabled"] = enabled
            if maximum_batching_window_in_seconds is not None:
                self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
            if maximum_record_age_in_seconds is not None:
                self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts
            if parallelization_factor is not None:
                self._values["parallelization_factor"] = parallelization_factor

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.DynamoDBEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bisect_batch_on_function_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnFunction.DynamoDBEventProperty.BisectBatchOnFunctionError``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("bisect_batch_on_function_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def destination_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.DestinationConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.DynamoDBEventProperty.DestinationConfig``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("destination_config")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.DestinationConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnFunction.DynamoDBEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumBatchingWindowInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_batching_window_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRecordAgeInSeconds``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_record_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.MaximumRetryAttempts``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelization_factor(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.DynamoDBEventProperty.ParallelizationFactor``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#dynamodb
            '''
            result = self._values.get("parallelization_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.EmptySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class EmptySAMPTProperty:
        def __init__(self) -> None:
            '''
            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnFunction.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnFunction.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnFunction.EventBridgeRuleEventProperty.Pattern``.

            :link: https://docs.aws.amazon.com/eventbridge/latest/userguide/filtering-examples-structure.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.EventBridgeRuleEventProperty.InputPath``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#eventbridgerule
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union["CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.ScheduleEventProperty", _IResolvable_da3f097b],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnFunction.EventSourceProperty.Properties``.
            :param type: ``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union["CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.ScheduleEventProperty", _IResolvable_da3f097b]:
            '''``CfnFunction.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union["CfnFunction.AlexaSkillEventProperty", "CfnFunction.ApiEventProperty", "CfnFunction.CloudWatchEventEventProperty", "CfnFunction.CloudWatchLogsEventProperty", "CfnFunction.DynamoDBEventProperty", "CfnFunction.EventBridgeRuleEventProperty", "CfnFunction.IoTRuleEventProperty", "CfnFunction.KinesisEventProperty", "CfnFunction.S3EventProperty", "CfnFunction.SNSEventProperty", "CfnFunction.SQSEventProperty", "CfnFunction.ScheduleEventProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnFunction.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.FileSystemConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "local_mount_path": "localMountPath"},
    )
    class FileSystemConfigProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            local_mount_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: ``CfnFunction.FileSystemConfigProperty.Arn``.
            :param local_mount_path: ``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if local_mount_path is not None:
                self._values["local_mount_path"] = local_mount_path

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.Arn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_mount_path(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.FileSystemConfigProperty.LocalMountPath``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-filesystemconfig.html#cfn-lambda-function-filesystemconfig-localmountpath
            '''
            result = self._values.get("local_mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.FunctionEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"variables": "variables"},
    )
    class FunctionEnvironmentProperty:
        def __init__(
            self,
            *,
            variables: typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]],
        ) -> None:
            '''
            :param variables: ``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "variables": variables,
            }

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]:
            '''``CfnFunction.FunctionEnvironmentProperty.Variables``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#environment-object
            '''
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnFunction.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.interface(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.IAMPolicyDocumentProperty"
    )
    class IAMPolicyDocumentProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
        '''

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Any:
            '''``CfnFunction.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            ...


    class _IAMPolicyDocumentPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
        '''

        __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_sam.CfnFunction.IAMPolicyDocumentProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Any:
            '''``CfnFunction.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            return typing.cast(typing.Any, jsii.get(self, "statement"))

    # Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
    typing.cast(typing.Any, IAMPolicyDocumentProperty).__jsii_proxy_class__ = lambda : _IAMPolicyDocumentPropertyProxy

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.IdentitySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"identity_name": "identityName"},
    )
    class IdentitySAMPTProperty:
        def __init__(self, *, identity_name: builtins.str) -> None:
            '''
            :param identity_name: ``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "identity_name": identity_name,
            }

        @builtins.property
        def identity_name(self) -> builtins.str:
            '''``CfnFunction.IdentitySAMPTProperty.IdentityName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("identity_name")
            assert result is not None, "Required property 'identity_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.IoTRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"sql": "sql", "aws_iot_sql_version": "awsIotSqlVersion"},
    )
    class IoTRuleEventProperty:
        def __init__(
            self,
            *,
            sql: builtins.str,
            aws_iot_sql_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param sql: ``CfnFunction.IoTRuleEventProperty.Sql``.
            :param aws_iot_sql_version: ``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "sql": sql,
            }
            if aws_iot_sql_version is not None:
                self._values["aws_iot_sql_version"] = aws_iot_sql_version

        @builtins.property
        def sql(self) -> builtins.str:
            '''``CfnFunction.IoTRuleEventProperty.Sql``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("sql")
            assert result is not None, "Required property 'sql' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_iot_sql_version(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.IoTRuleEventProperty.AwsIotSqlVersion``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#iotrule
            '''
            result = self._values.get("aws_iot_sql_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.KeySAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId"},
    )
    class KeySAMPTProperty:
        def __init__(self, *, key_id: builtins.str) -> None:
            '''
            :param key_id: ``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key_id": key_id,
            }

        @builtins.property
        def key_id(self) -> builtins.str:
            '''``CfnFunction.KeySAMPTProperty.KeyId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeySAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.KinesisEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "starting_position": "startingPosition",
            "stream": "stream",
            "batch_size": "batchSize",
            "enabled": "enabled",
        },
    )
    class KinesisEventProperty:
        def __init__(
            self,
            *,
            starting_position: builtins.str,
            stream: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param starting_position: ``CfnFunction.KinesisEventProperty.StartingPosition``.
            :param stream: ``CfnFunction.KinesisEventProperty.Stream``.
            :param batch_size: ``CfnFunction.KinesisEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.KinesisEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "starting_position": starting_position,
                "stream": stream,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def starting_position(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.StartingPosition``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("starting_position")
            assert result is not None, "Required property 'starting_position' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stream(self) -> builtins.str:
            '''``CfnFunction.KinesisEventProperty.Stream``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("stream")
            assert result is not None, "Required property 'stream' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.KinesisEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnFunction.KinesisEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#kinesis
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.LogGroupSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogGroupSAMPTProperty:
        def __init__(self, *, log_group_name: builtins.str) -> None:
            '''
            :param log_group_name: ``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "log_group_name": log_group_name,
            }

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''``CfnFunction.LogGroupSAMPTProperty.LogGroupName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogGroupSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.OnFailureProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "type": "type"},
    )
    class OnFailureProperty:
        def __init__(
            self,
            *,
            destination: builtins.str,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: ``CfnFunction.OnFailureProperty.Destination``.
            :param type: ``CfnFunction.OnFailureProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
            }
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination(self) -> builtins.str:
            '''``CfnFunction.OnFailureProperty.Destination``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.OnFailureProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#destination-config-object
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnFailureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.ProvisionedConcurrencyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_concurrent_executions": "provisionedConcurrentExecutions",
        },
    )
    class ProvisionedConcurrencyConfigProperty:
        def __init__(self, *, provisioned_concurrent_executions: builtins.str) -> None:
            '''
            :param provisioned_concurrent_executions: ``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "provisioned_concurrent_executions": provisioned_concurrent_executions,
            }

        @builtins.property
        def provisioned_concurrent_executions(self) -> builtins.str:
            '''``CfnFunction.ProvisionedConcurrencyConfigProperty.ProvisionedConcurrentExecutions``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#provisioned-concurrency-config-object
            '''
            result = self._values.get("provisioned_concurrent_executions")
            assert result is not None, "Required property 'provisioned_concurrent_executions' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedConcurrencyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.QueueSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"queue_name": "queueName"},
    )
    class QueueSAMPTProperty:
        def __init__(self, *, queue_name: builtins.str) -> None:
            '''
            :param queue_name: ``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "queue_name": queue_name,
            }

        @builtins.property
        def queue_name(self) -> builtins.str:
            '''``CfnFunction.QueueSAMPTProperty.QueueName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("queue_name")
            assert result is not None, "Required property 'queue_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.S3EventProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "events": "events", "filter": "filter"},
    )
    class S3EventProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            events: typing.Union[builtins.str, _IResolvable_da3f097b, typing.Sequence[builtins.str]],
            filter: typing.Optional[typing.Union["CfnFunction.S3NotificationFilterProperty", _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3EventProperty.Bucket``.
            :param events: ``CfnFunction.S3EventProperty.Events``.
            :param filter: ``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "events": events,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3EventProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def events(
            self,
        ) -> typing.Union[builtins.str, _IResolvable_da3f097b, typing.List[builtins.str]]:
            '''``CfnFunction.S3EventProperty.Events``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("events")
            assert result is not None, "Required property 'events' is missing"
            return typing.cast(typing.Union[builtins.str, _IResolvable_da3f097b, typing.List[builtins.str]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.S3NotificationFilterProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.S3EventProperty.Filter``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.S3NotificationFilterProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnFunction.S3KeyFilterRuleProperty", _IResolvable_da3f097b]]],
        ) -> None:
            '''
            :param rules: ``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnFunction.S3KeyFilterRuleProperty", _IResolvable_da3f097b]]]:
            '''``CfnFunction.S3KeyFilterProperty.Rules``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnFunction.S3KeyFilterRuleProperty", _IResolvable_da3f097b]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.S3KeyFilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class S3KeyFilterRuleProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''
            :param name: ``CfnFunction.S3KeyFilterRuleProperty.Name``.
            :param value: ``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Name``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnFunction.S3KeyFilterRuleProperty.Value``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnFunction.S3LocationProperty.Bucket``.
            :param key: ``CfnFunction.S3LocationProperty.Key``.
            :param version: ``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnFunction.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.S3NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class S3NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Union["CfnFunction.S3KeyFilterProperty", _IResolvable_da3f097b],
        ) -> None:
            '''
            :param s3_key: ``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Union["CfnFunction.S3KeyFilterProperty", _IResolvable_da3f097b]:
            '''``CfnFunction.S3NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(typing.Union["CfnFunction.S3KeyFilterProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ami_describe_policy": "amiDescribePolicy",
            "cloud_formation_describe_stacks_policy": "cloudFormationDescribeStacksPolicy",
            "cloud_watch_put_metric_policy": "cloudWatchPutMetricPolicy",
            "dynamo_db_crud_policy": "dynamoDbCrudPolicy",
            "dynamo_db_read_policy": "dynamoDbReadPolicy",
            "dynamo_db_stream_read_policy": "dynamoDbStreamReadPolicy",
            "ec2_describe_policy": "ec2DescribePolicy",
            "elasticsearch_http_post_policy": "elasticsearchHttpPostPolicy",
            "filter_log_events_policy": "filterLogEventsPolicy",
            "kinesis_crud_policy": "kinesisCrudPolicy",
            "kinesis_stream_read_policy": "kinesisStreamReadPolicy",
            "kms_decrypt_policy": "kmsDecryptPolicy",
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "rekognition_detect_only_policy": "rekognitionDetectOnlyPolicy",
            "rekognition_labels_policy": "rekognitionLabelsPolicy",
            "rekognition_no_data_access_policy": "rekognitionNoDataAccessPolicy",
            "rekognition_read_policy": "rekognitionReadPolicy",
            "rekognition_write_only_access_policy": "rekognitionWriteOnlyAccessPolicy",
            "s3_crud_policy": "s3CrudPolicy",
            "s3_read_policy": "s3ReadPolicy",
            "ses_bulk_templated_crud_policy": "sesBulkTemplatedCrudPolicy",
            "ses_crud_policy": "sesCrudPolicy",
            "ses_email_template_crud_policy": "sesEmailTemplateCrudPolicy",
            "ses_send_bounce_policy": "sesSendBouncePolicy",
            "sns_crud_policy": "snsCrudPolicy",
            "sns_publish_message_policy": "snsPublishMessagePolicy",
            "sqs_poller_policy": "sqsPollerPolicy",
            "sqs_send_message_policy": "sqsSendMessagePolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
            "vpc_access_policy": "vpcAccessPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            ami_describe_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            cloud_formation_describe_stacks_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            cloud_watch_put_metric_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            dynamo_db_crud_policy: typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]] = None,
            dynamo_db_read_policy: typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]] = None,
            dynamo_db_stream_read_policy: typing.Optional[typing.Union["CfnFunction.TableStreamSAMPTProperty", _IResolvable_da3f097b]] = None,
            ec2_describe_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            elasticsearch_http_post_policy: typing.Optional[typing.Union["CfnFunction.DomainSAMPTProperty", _IResolvable_da3f097b]] = None,
            filter_log_events_policy: typing.Optional[typing.Union["CfnFunction.LogGroupSAMPTProperty", _IResolvable_da3f097b]] = None,
            kinesis_crud_policy: typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]] = None,
            kinesis_stream_read_policy: typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]] = None,
            kms_decrypt_policy: typing.Optional[typing.Union["CfnFunction.KeySAMPTProperty", _IResolvable_da3f097b]] = None,
            lambda_invoke_policy: typing.Optional[typing.Union["CfnFunction.FunctionSAMPTProperty", _IResolvable_da3f097b]] = None,
            rekognition_detect_only_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            rekognition_labels_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            rekognition_no_data_access_policy: typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]] = None,
            rekognition_read_policy: typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]] = None,
            rekognition_write_only_access_policy: typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]] = None,
            s3_crud_policy: typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]] = None,
            s3_read_policy: typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]] = None,
            ses_bulk_templated_crud_policy: typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]] = None,
            ses_crud_policy: typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]] = None,
            ses_email_template_crud_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
            ses_send_bounce_policy: typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]] = None,
            sns_crud_policy: typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]] = None,
            sns_publish_message_policy: typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]] = None,
            sqs_poller_policy: typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]] = None,
            sqs_send_message_policy: typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union["CfnFunction.StateMachineSAMPTProperty", _IResolvable_da3f097b]] = None,
            vpc_access_policy: typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param ami_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.
            :param cloud_formation_describe_stacks_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.
            :param cloud_watch_put_metric_policy: ``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.
            :param dynamo_db_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.
            :param dynamo_db_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.
            :param dynamo_db_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.
            :param ec2_describe_policy: ``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.
            :param elasticsearch_http_post_policy: ``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.
            :param filter_log_events_policy: ``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.
            :param kinesis_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.
            :param kinesis_stream_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.
            :param kms_decrypt_policy: ``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.
            :param lambda_invoke_policy: ``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param rekognition_detect_only_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.
            :param rekognition_labels_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.
            :param rekognition_no_data_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.
            :param rekognition_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.
            :param rekognition_write_only_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.
            :param s3_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.
            :param s3_read_policy: ``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.
            :param ses_bulk_templated_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.
            :param ses_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.
            :param ses_email_template_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.
            :param ses_send_bounce_policy: ``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.
            :param sns_crud_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.
            :param sns_publish_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.
            :param sqs_poller_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.
            :param sqs_send_message_policy: ``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.
            :param step_functions_execution_policy: ``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.
            :param vpc_access_policy: ``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if ami_describe_policy is not None:
                self._values["ami_describe_policy"] = ami_describe_policy
            if cloud_formation_describe_stacks_policy is not None:
                self._values["cloud_formation_describe_stacks_policy"] = cloud_formation_describe_stacks_policy
            if cloud_watch_put_metric_policy is not None:
                self._values["cloud_watch_put_metric_policy"] = cloud_watch_put_metric_policy
            if dynamo_db_crud_policy is not None:
                self._values["dynamo_db_crud_policy"] = dynamo_db_crud_policy
            if dynamo_db_read_policy is not None:
                self._values["dynamo_db_read_policy"] = dynamo_db_read_policy
            if dynamo_db_stream_read_policy is not None:
                self._values["dynamo_db_stream_read_policy"] = dynamo_db_stream_read_policy
            if ec2_describe_policy is not None:
                self._values["ec2_describe_policy"] = ec2_describe_policy
            if elasticsearch_http_post_policy is not None:
                self._values["elasticsearch_http_post_policy"] = elasticsearch_http_post_policy
            if filter_log_events_policy is not None:
                self._values["filter_log_events_policy"] = filter_log_events_policy
            if kinesis_crud_policy is not None:
                self._values["kinesis_crud_policy"] = kinesis_crud_policy
            if kinesis_stream_read_policy is not None:
                self._values["kinesis_stream_read_policy"] = kinesis_stream_read_policy
            if kms_decrypt_policy is not None:
                self._values["kms_decrypt_policy"] = kms_decrypt_policy
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if rekognition_detect_only_policy is not None:
                self._values["rekognition_detect_only_policy"] = rekognition_detect_only_policy
            if rekognition_labels_policy is not None:
                self._values["rekognition_labels_policy"] = rekognition_labels_policy
            if rekognition_no_data_access_policy is not None:
                self._values["rekognition_no_data_access_policy"] = rekognition_no_data_access_policy
            if rekognition_read_policy is not None:
                self._values["rekognition_read_policy"] = rekognition_read_policy
            if rekognition_write_only_access_policy is not None:
                self._values["rekognition_write_only_access_policy"] = rekognition_write_only_access_policy
            if s3_crud_policy is not None:
                self._values["s3_crud_policy"] = s3_crud_policy
            if s3_read_policy is not None:
                self._values["s3_read_policy"] = s3_read_policy
            if ses_bulk_templated_crud_policy is not None:
                self._values["ses_bulk_templated_crud_policy"] = ses_bulk_templated_crud_policy
            if ses_crud_policy is not None:
                self._values["ses_crud_policy"] = ses_crud_policy
            if ses_email_template_crud_policy is not None:
                self._values["ses_email_template_crud_policy"] = ses_email_template_crud_policy
            if ses_send_bounce_policy is not None:
                self._values["ses_send_bounce_policy"] = ses_send_bounce_policy
            if sns_crud_policy is not None:
                self._values["sns_crud_policy"] = sns_crud_policy
            if sns_publish_message_policy is not None:
                self._values["sns_publish_message_policy"] = sns_publish_message_policy
            if sqs_poller_policy is not None:
                self._values["sqs_poller_policy"] = sqs_poller_policy
            if sqs_send_message_policy is not None:
                self._values["sqs_send_message_policy"] = sqs_send_message_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy
            if vpc_access_policy is not None:
                self._values["vpc_access_policy"] = vpc_access_policy

        @builtins.property
        def ami_describe_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.AMIDescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ami_describe_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def cloud_formation_describe_stacks_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudFormationDescribeStacksPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_formation_describe_stacks_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def cloud_watch_put_metric_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.CloudWatchPutMetricPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("cloud_watch_put_metric_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def dynamo_db_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def dynamo_db_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def dynamo_db_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TableStreamSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.DynamoDBStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("dynamo_db_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TableStreamSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def ec2_describe_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.EC2DescribePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ec2_describe_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def elasticsearch_http_post_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.DomainSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.ElasticsearchHttpPostPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("elasticsearch_http_post_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.DomainSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def filter_log_events_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.LogGroupSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.FilterLogEventsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("filter_log_events_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.LogGroupSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def kinesis_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def kinesis_stream_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KinesisStreamReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kinesis_stream_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StreamSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def kms_decrypt_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.KeySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.KMSDecryptPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("kms_decrypt_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.KeySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.FunctionSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.FunctionSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def rekognition_detect_only_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionDetectOnlyPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_detect_only_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def rekognition_labels_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionLabelsPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_labels_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def rekognition_no_data_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionNoDataAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_no_data_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def rekognition_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def rekognition_write_only_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.RekognitionWriteOnlyAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("rekognition_write_only_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.CollectionSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def s3_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3CrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def s3_read_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.S3ReadPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("s3_read_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.BucketSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def ses_bulk_templated_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESBulkTemplatedCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_bulk_templated_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def ses_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def ses_email_template_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESEmailTemplateCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_email_template_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def ses_send_bounce_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SESSendBouncePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("ses_send_bounce_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.IdentitySAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def sns_crud_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSCrudPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_crud_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def sns_publish_message_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SNSPublishMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sns_publish_message_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.TopicSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def sqs_poller_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSPollerPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_poller_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def sqs_send_message_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.SQSSendMessagePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("sqs_send_message_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.QueueSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.StateMachineSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.StateMachineSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def vpc_access_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnFunction.SAMPolicyTemplateProperty.VPCAccessPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("vpc_access_policy")
            return typing.cast(typing.Optional[typing.Union["CfnFunction.EmptySAMPTProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.SNSEventProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic"},
    )
    class SNSEventProperty:
        def __init__(self, *, topic: builtins.str) -> None:
            '''
            :param topic: ``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "topic": topic,
            }

        @builtins.property
        def topic(self) -> builtins.str:
            '''``CfnFunction.SNSEventProperty.Topic``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sns
            '''
            result = self._values.get("topic")
            assert result is not None, "Required property 'topic' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.SQSEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "queue": "queue",
            "batch_size": "batchSize",
            "enabled": "enabled",
        },
    )
    class SQSEventProperty:
        def __init__(
            self,
            *,
            queue: builtins.str,
            batch_size: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param queue: ``CfnFunction.SQSEventProperty.Queue``.
            :param batch_size: ``CfnFunction.SQSEventProperty.BatchSize``.
            :param enabled: ``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "queue": queue,
            }
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def queue(self) -> builtins.str:
            '''``CfnFunction.SQSEventProperty.Queue``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("queue")
            assert result is not None, "Required property 'queue' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnFunction.SQSEventProperty.BatchSize``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnFunction.SQSEventProperty.Enabled``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#sqs
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SQSEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule", "input": "input"},
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            input: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnFunction.ScheduleEventProperty.Schedule``.
            :param input: ``CfnFunction.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "schedule": schedule,
            }
            if input is not None:
                self._values["input"] = input

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnFunction.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnFunction.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnFunction.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.StreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName"},
    )
    class StreamSAMPTProperty:
        def __init__(self, *, stream_name: builtins.str) -> None:
            '''
            :param stream_name: ``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "stream_name": stream_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.StreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.TableSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName"},
    )
    class TableSAMPTProperty:
        def __init__(self, *, table_name: builtins.str) -> None:
            '''
            :param table_name: ``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "table_name": table_name,
            }

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.TableStreamSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_name": "streamName", "table_name": "tableName"},
    )
    class TableStreamSAMPTProperty:
        def __init__(
            self,
            *,
            stream_name: builtins.str,
            table_name: builtins.str,
        ) -> None:
            '''
            :param stream_name: ``CfnFunction.TableStreamSAMPTProperty.StreamName``.
            :param table_name: ``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "stream_name": stream_name,
                "table_name": table_name,
            }

        @builtins.property
        def stream_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.StreamName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("stream_name")
            assert result is not None, "Required property 'stream_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''``CfnFunction.TableStreamSAMPTProperty.TableName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableStreamSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.TopicSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_name": "topicName"},
    )
    class TopicSAMPTProperty:
        def __init__(self, *, topic_name: builtins.str) -> None:
            '''
            :param topic_name: ``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "topic_name": topic_name,
            }

        @builtins.property
        def topic_name(self) -> builtins.str:
            '''``CfnFunction.TopicSAMPTProperty.TopicName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("topic_name")
            assert result is not None, "Required property 'topic_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnFunction.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param security_group_ids: ``CfnFunction.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SecurityGroupIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''``CfnFunction.VpcConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "code_uri": "codeUri",
        "handler": "handler",
        "runtime": "runtime",
        "auto_publish_alias": "autoPublishAlias",
        "dead_letter_queue": "deadLetterQueue",
        "deployment_preference": "deploymentPreference",
        "description": "description",
        "environment": "environment",
        "events": "events",
        "file_system_configs": "fileSystemConfigs",
        "function_name": "functionName",
        "kms_key_arn": "kmsKeyArn",
        "layers": "layers",
        "memory_size": "memorySize",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "provisioned_concurrency_config": "provisionedConcurrencyConfig",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "tags": "tags",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc_config": "vpcConfig",
    },
)
class CfnFunctionProps:
    def __init__(
        self,
        *,
        code_uri: typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_da3f097b],
        handler: builtins.str,
        runtime: builtins.str,
        auto_publish_alias: typing.Optional[builtins.str] = None,
        dead_letter_queue: typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_da3f097b]] = None,
        deployment_preference: typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_da3f097b]] = None,
        events: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_da3f097b]]]] = None,
        file_system_configs: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_da3f097b]]]] = None,
        function_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        layers: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.Sequence[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]] = None,
        provisioned_concurrency_config: typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_da3f097b]] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        tracing: typing.Optional[builtins.str] = None,
        vpc_config: typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::Function``.

        :param code_uri: ``AWS::Serverless::Function.CodeUri``.
        :param handler: ``AWS::Serverless::Function.Handler``.
        :param runtime: ``AWS::Serverless::Function.Runtime``.
        :param auto_publish_alias: ``AWS::Serverless::Function.AutoPublishAlias``.
        :param dead_letter_queue: ``AWS::Serverless::Function.DeadLetterQueue``.
        :param deployment_preference: ``AWS::Serverless::Function.DeploymentPreference``.
        :param description: ``AWS::Serverless::Function.Description``.
        :param environment: ``AWS::Serverless::Function.Environment``.
        :param events: ``AWS::Serverless::Function.Events``.
        :param file_system_configs: ``AWS::Serverless::Function.FileSystemConfigs``.
        :param function_name: ``AWS::Serverless::Function.FunctionName``.
        :param kms_key_arn: ``AWS::Serverless::Function.KmsKeyArn``.
        :param layers: ``AWS::Serverless::Function.Layers``.
        :param memory_size: ``AWS::Serverless::Function.MemorySize``.
        :param permissions_boundary: ``AWS::Serverless::Function.PermissionsBoundary``.
        :param policies: ``AWS::Serverless::Function.Policies``.
        :param provisioned_concurrency_config: ``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.
        :param reserved_concurrent_executions: ``AWS::Serverless::Function.ReservedConcurrentExecutions``.
        :param role: ``AWS::Serverless::Function.Role``.
        :param tags: ``AWS::Serverless::Function.Tags``.
        :param timeout: ``AWS::Serverless::Function.Timeout``.
        :param tracing: ``AWS::Serverless::Function.Tracing``.
        :param vpc_config: ``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "code_uri": code_uri,
            "handler": handler,
            "runtime": runtime,
        }
        if auto_publish_alias is not None:
            self._values["auto_publish_alias"] = auto_publish_alias
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if deployment_preference is not None:
            self._values["deployment_preference"] = deployment_preference
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if events is not None:
            self._values["events"] = events
        if file_system_configs is not None:
            self._values["file_system_configs"] = file_system_configs
        if function_name is not None:
            self._values["function_name"] = function_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if layers is not None:
            self._values["layers"] = layers
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if provisioned_concurrency_config is not None:
            self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def code_uri(
        self,
    ) -> typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_da3f097b]:
        '''``AWS::Serverless::Function.CodeUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("code_uri")
        assert result is not None, "Required property 'code_uri' is missing"
        return typing.cast(typing.Union[builtins.str, CfnFunction.S3LocationProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''``AWS::Serverless::Function.Handler``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''``AWS::Serverless::Function.Runtime``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_publish_alias(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.AutoPublishAlias``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("auto_publish_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dead_letter_queue(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.DeadLetterQueue``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.DeadLetterQueueProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def deployment_preference(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.DeploymentPreference``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#deploymentpreference-object
        '''
        result = self._values.get("deployment_preference")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.DeploymentPreferenceProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.Environment``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.FunctionEnvironmentProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.Events``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnFunction.EventSourceProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def file_system_configs(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.FileSystemConfigs``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html
        '''
        result = self._values.get("file_system_configs")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnFunction.FileSystemConfigProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.FunctionName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.KmsKeyArn``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::Function.Layers``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.MemorySize``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.PermissionsBoundary``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::Function.Policies``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, CfnFunction.IAMPolicyDocumentProperty, CfnFunction.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def provisioned_concurrency_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.ProvisionedConcurrencyConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("provisioned_concurrency_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.ProvisionedConcurrencyConfigProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.ReservedConcurrentExecutions``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Role``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::Function.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Serverless::Function.Timeout``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tracing(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::Function.Tracing``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::Function.VpcConfig``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunction.VpcConfigProperty, _IResolvable_da3f097b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnLayerVersion(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnLayerVersion",
):
    '''A CloudFormation ``AWS::Serverless::LayerVersion``.

    :cloudformationResource: AWS::Serverless::LayerVersion
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::LayerVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.
        '''
        props = CfnLayerVersionProps(
            compatible_runtimes=compatible_runtimes,
            content_uri=content_uri,
            description=description,
            layer_name=layer_name,
            license_info=license_info,
            retention_policy=retention_policy,
        )

        jsii.create(CfnLayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "compatibleRuntimes"))

    @compatible_runtimes.setter
    def compatible_runtimes(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "compatibleRuntimes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentUri")
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_da3f097b]], jsii.get(self, "contentUri"))

    @content_uri.setter
    def content_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnLayerVersion.S3LocationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "contentUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="layerName")
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "layerName"))

    @layer_name.setter
    def layer_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "layerName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="licenseInfo")
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInfo"))

    @license_info.setter
    def license_info(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "licenseInfo", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionPolicy"))

    @retention_policy.setter
    def retention_policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "retentionPolicy", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnLayerVersion.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnLayerVersion.S3LocationProperty.Bucket``.
            :param key: ``CfnLayerVersion.S3LocationProperty.Key``.
            :param version: ``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnLayerVersion.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnLayerVersion.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnLayerVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "compatible_runtimes": "compatibleRuntimes",
        "content_uri": "contentUri",
        "description": "description",
        "layer_name": "layerName",
        "license_info": "licenseInfo",
        "retention_policy": "retentionPolicy",
    },
)
class CfnLayerVersionProps:
    def __init__(
        self,
        *,
        compatible_runtimes: typing.Optional[typing.Sequence[builtins.str]] = None,
        content_uri: typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_name: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::LayerVersion``.

        :param compatible_runtimes: ``AWS::Serverless::LayerVersion.CompatibleRuntimes``.
        :param content_uri: ``AWS::Serverless::LayerVersion.ContentUri``.
        :param description: ``AWS::Serverless::LayerVersion.Description``.
        :param layer_name: ``AWS::Serverless::LayerVersion.LayerName``.
        :param license_info: ``AWS::Serverless::LayerVersion.LicenseInfo``.
        :param retention_policy: ``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes
        if content_uri is not None:
            self._values["content_uri"] = content_uri
        if description is not None:
            self._values["description"] = description
        if layer_name is not None:
            self._values["layer_name"] = layer_name
        if license_info is not None:
            self._values["license_info"] = license_info
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Serverless::LayerVersion.CompatibleRuntimes``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::LayerVersion.ContentUri``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("content_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnLayerVersion.S3LocationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.Description``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LayerName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("layer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.LicenseInfo``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::LayerVersion.RetentionPolicy``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesslayerversion
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnSimpleTable(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnSimpleTable",
):
    '''A CloudFormation ``AWS::Serverless::SimpleTable``.

    :cloudformationResource: AWS::Serverless::SimpleTable
    :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        primary_key: typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_da3f097b]] = None,
        provisioned_throughput: typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_da3f097b]] = None,
        sse_specification: typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_da3f097b]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::SimpleTable``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.
        '''
        props = CfnSimpleTableProps(
            primary_key=primary_key,
            provisioned_throughput=provisioned_throughput,
            sse_specification=sse_specification,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(CfnSimpleTable, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="primaryKey")
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_da3f097b]], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.PrimaryKeyProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "primaryKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provisionedThroughput")
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_da3f097b]], jsii.get(self, "provisionedThroughput"))

    @provisioned_throughput.setter
    def provisioned_throughput(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.ProvisionedThroughputProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "provisionedThroughput", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_da3f097b]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnSimpleTable.SSESpecificationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "sseSpecification", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tableName", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnSimpleTable.PrimaryKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "name": "name"},
    )
    class PrimaryKeyProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: ``CfnSimpleTable.PrimaryKeyProperty.Type``.
            :param name: ``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnSimpleTable.PrimaryKeyProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnSimpleTable.PrimaryKeyProperty.Name``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnSimpleTable.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "write_capacity_units": "writeCapacityUnits",
            "read_capacity_units": "readCapacityUnits",
        },
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            write_capacity_units: jsii.Number,
            read_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param write_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.
            :param read_capacity_units: ``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "write_capacity_units": write_capacity_units,
            }
            if read_capacity_units is not None:
                self._values["read_capacity_units"] = read_capacity_units

        @builtins.property
        def write_capacity_units(self) -> jsii.Number:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.WriteCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("write_capacity_units")
            assert result is not None, "Required property 'write_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def read_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''``CfnSimpleTable.ProvisionedThroughputProperty.ReadCapacityUnits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
            '''
            result = self._values.get("read_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedThroughputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnSimpleTable.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param sse_enabled: ``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnSimpleTable.SSESpecificationProperty.SSEEnabled``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-table-ssespecification.html
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnSimpleTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "primary_key": "primaryKey",
        "provisioned_throughput": "provisionedThroughput",
        "sse_specification": "sseSpecification",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnSimpleTableProps:
    def __init__(
        self,
        *,
        primary_key: typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_da3f097b]] = None,
        provisioned_throughput: typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_da3f097b]] = None,
        sse_specification: typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_da3f097b]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::SimpleTable``.

        :param primary_key: ``AWS::Serverless::SimpleTable.PrimaryKey``.
        :param provisioned_throughput: ``AWS::Serverless::SimpleTable.ProvisionedThroughput``.
        :param sse_specification: ``AWS::Serverless::SimpleTable.SSESpecification``.
        :param table_name: ``AWS::Serverless::SimpleTable.TableName``.
        :param tags: ``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if primary_key is not None:
            self._values["primary_key"] = primary_key
        if provisioned_throughput is not None:
            self._values["provisioned_throughput"] = provisioned_throughput
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.PrimaryKey``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#primary-key-object
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.PrimaryKeyProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def provisioned_throughput(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.ProvisionedThroughput``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-provisionedthroughput.html
        '''
        result = self._values.get("provisioned_throughput")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.ProvisionedThroughputProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::SimpleTable.SSESpecification``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnSimpleTable.SSESpecificationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::SimpleTable.TableName``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::SimpleTable.Tags``.

        :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlesssimpletable
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimpleTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnStateMachine(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine",
):
    '''A CloudFormation ``AWS::Serverless::StateMachine``.

    :cloudformationResource: AWS::Serverless::StateMachine
    :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_da3f097b]] = None,
        events: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_da3f097b]]]] = None,
        logging: typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.Sequence[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Serverless::StateMachine``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param type: ``AWS::Serverless::StateMachine.Type``.
        '''
        props = CfnStateMachineProps(
            definition=definition,
            definition_substitutions=definition_substitutions,
            definition_uri=definition_uri,
            events=events,
            logging=logging,
            name=name,
            policies=policies,
            role=role,
            tags=tags,
            type=type,
        )

        jsii.create(CfnStateMachine, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="REQUIRED_TRANSFORM")
    def REQUIRED_TRANSFORM(cls) -> builtins.str:
        '''The ``Transform`` a template must use in order to use this resource.'''
        return typing.cast(builtins.str, jsii.sget(cls, "REQUIRED_TRANSFORM"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Any, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Any) -> None:
        jsii.set(self, "definition", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionSubstitutions")
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "definitionSubstitutions"))

    @definition_substitutions.setter
    def definition_substitutions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "definitionSubstitutions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_da3f097b]], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.S3LocationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "definitionUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_da3f097b]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnStateMachine.EventSourceProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "events", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logging")
    def logging(
        self,
    ) -> typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "logging"))

    @logging.setter
    def logging(
        self,
        value: typing.Optional[typing.Union["CfnStateMachine.LoggingConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "logging", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, "CfnStateMachine.IAMPolicyDocumentProperty", "CfnStateMachine.SAMPolicyTemplateProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "policies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "role"))

    @role.setter
    def role(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "role", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.ApiEventProperty",
        jsii_struct_bases=[],
        name_mapping={"method": "method", "path": "path", "rest_api_id": "restApiId"},
    )
    class ApiEventProperty:
        def __init__(
            self,
            *,
            method: builtins.str,
            path: builtins.str,
            rest_api_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param method: ``CfnStateMachine.ApiEventProperty.Method``.
            :param path: ``CfnStateMachine.ApiEventProperty.Path``.
            :param rest_api_id: ``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "method": method,
                "path": path,
            }
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id

        @builtins.property
        def method(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Method``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("method")
            assert result is not None, "Required property 'method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def path(self) -> builtins.str:
            '''``CfnStateMachine.ApiEventProperty.Path``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ApiEventProperty.RestApiId``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.CloudWatchEventEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class CloudWatchEventEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.CloudWatchEventEventProperty.Input``.
            :param input_path: ``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.CloudWatchEventEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEventEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.CloudWatchLogsLogGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsLogGroupProperty:
        def __init__(self, *, log_group_arn: builtins.str) -> None:
            '''
            :param log_group_arn: ``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "log_group_arn": log_group_arn,
            }

        @builtins.property
        def log_group_arn(self) -> builtins.str:
            '''``CfnStateMachine.CloudWatchLogsLogGroupProperty.LogGroupArn``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup.html
            '''
            result = self._values.get("log_group_arn")
            assert result is not None, "Required property 'log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.EventBridgeRuleEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "event_bus_name": "eventBusName",
            "input": "input",
            "input_path": "inputPath",
        },
    )
    class EventBridgeRuleEventProperty:
        def __init__(
            self,
            *,
            pattern: typing.Any,
            event_bus_name: typing.Optional[builtins.str] = None,
            input: typing.Optional[builtins.str] = None,
            input_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param pattern: ``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.
            :param event_bus_name: ``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.
            :param input: ``CfnStateMachine.EventBridgeRuleEventProperty.Input``.
            :param input_path: ``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
            }
            if event_bus_name is not None:
                self._values["event_bus_name"] = event_bus_name
            if input is not None:
                self._values["input"] = input
            if input_path is not None:
                self._values["input_path"] = input_path

        @builtins.property
        def pattern(self) -> typing.Any:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Pattern``.

            :link: http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
            '''
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_bus_name(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.EventBusName``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("event_bus_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.Input``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_path(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.EventBridgeRuleEventProperty.InputPath``.

            :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-statemachine-cloudwatchevent.html
            '''
            result = self._values.get("input_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeRuleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.EventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"properties": "properties", "type": "type"},
    )
    class EventSourceProperty:
        def __init__(
            self,
            *,
            properties: typing.Union["CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty", _IResolvable_da3f097b],
            type: builtins.str,
        ) -> None:
            '''
            :param properties: ``CfnStateMachine.EventSourceProperty.Properties``.
            :param type: ``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "properties": properties,
                "type": type,
            }

        @builtins.property
        def properties(
            self,
        ) -> typing.Union["CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty", _IResolvable_da3f097b]:
            '''``CfnStateMachine.EventSourceProperty.Properties``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-types
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union["CfnStateMachine.ApiEventProperty", "CfnStateMachine.CloudWatchEventEventProperty", "CfnStateMachine.EventBridgeRuleEventProperty", "CfnStateMachine.ScheduleEventProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnStateMachine.EventSourceProperty.Type``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#event-source-object
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.FunctionSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"function_name": "functionName"},
    )
    class FunctionSAMPTProperty:
        def __init__(self, *, function_name: builtins.str) -> None:
            '''
            :param function_name: ``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "function_name": function_name,
            }

        @builtins.property
        def function_name(self) -> builtins.str:
            '''``CfnStateMachine.FunctionSAMPTProperty.FunctionName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("function_name")
            assert result is not None, "Required property 'function_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.interface(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.IAMPolicyDocumentProperty"
    )
    class IAMPolicyDocumentProperty(typing_extensions.Protocol):
        '''
        :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
        '''

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Any:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            ...


    class _IAMPolicyDocumentPropertyProxy:
        '''
        :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
        '''

        __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_sam.CfnStateMachine.IAMPolicyDocumentProperty"

        @builtins.property # type: ignore[misc]
        @jsii.member(jsii_name="statement")
        def statement(self) -> typing.Any:
            '''``CfnStateMachine.IAMPolicyDocumentProperty.Statement``.

            :link: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
            '''
            return typing.cast(typing.Any, jsii.get(self, "statement"))

    # Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
    typing.cast(typing.Any, IAMPolicyDocumentProperty).__jsii_proxy_class__ = lambda : _IAMPolicyDocumentPropertyProxy

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.LogDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_logs_log_group": "cloudWatchLogsLogGroup"},
    )
    class LogDestinationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group: typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_da3f097b],
        ) -> None:
            '''
            :param cloud_watch_logs_log_group: ``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cloud_watch_logs_log_group": cloud_watch_logs_log_group,
            }

        @builtins.property
        def cloud_watch_logs_log_group(
            self,
        ) -> typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_da3f097b]:
            '''``CfnStateMachine.LogDestinationProperty.CloudWatchLogsLogGroup``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-logdestination.html#cfn-stepfunctions-statemachine-logdestination-cloudwatchlogsloggroup
            '''
            result = self._values.get("cloud_watch_logs_log_group")
            assert result is not None, "Required property 'cloud_watch_logs_log_group' is missing"
            return typing.cast(typing.Union["CfnStateMachine.CloudWatchLogsLogGroupProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destinations": "destinations",
            "include_execution_data": "includeExecutionData",
            "level": "level",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destinations: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_da3f097b]]],
            include_execution_data: typing.Union[builtins.bool, _IResolvable_da3f097b],
            level: builtins.str,
        ) -> None:
            '''
            :param destinations: ``CfnStateMachine.LoggingConfigurationProperty.Destinations``.
            :param include_execution_data: ``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.
            :param level: ``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destinations": destinations,
                "include_execution_data": include_execution_data,
                "level": level,
            }

        @builtins.property
        def destinations(
            self,
        ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_da3f097b]]]:
            '''``CfnStateMachine.LoggingConfigurationProperty.Destinations``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("destinations")
            assert result is not None, "Required property 'destinations' is missing"
            return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnStateMachine.LogDestinationProperty", _IResolvable_da3f097b]]], result)

        @builtins.property
        def include_execution_data(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_da3f097b]:
            '''``CfnStateMachine.LoggingConfigurationProperty.IncludeExecutionData``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("include_execution_data")
            assert result is not None, "Required property 'include_execution_data' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_da3f097b], result)

        @builtins.property
        def level(self) -> builtins.str:
            '''``CfnStateMachine.LoggingConfigurationProperty.Level``.

            :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-stepfunctions-statemachine-loggingconfiguration.html
            '''
            result = self._values.get("level")
            assert result is not None, "Required property 'level' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key", "version": "version"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param bucket: ``CfnStateMachine.S3LocationProperty.Bucket``.
            :param key: ``CfnStateMachine.S3LocationProperty.Key``.
            :param version: ``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#s3-location-object
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Bucket``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnStateMachine.S3LocationProperty.Key``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''``CfnStateMachine.S3LocationProperty.Version``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.SAMPolicyTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_invoke_policy": "lambdaInvokePolicy",
            "step_functions_execution_policy": "stepFunctionsExecutionPolicy",
        },
    )
    class SAMPolicyTemplateProperty:
        def __init__(
            self,
            *,
            lambda_invoke_policy: typing.Optional[typing.Union["CfnStateMachine.FunctionSAMPTProperty", _IResolvable_da3f097b]] = None,
            step_functions_execution_policy: typing.Optional[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param lambda_invoke_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.
            :param step_functions_execution_policy: ``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if lambda_invoke_policy is not None:
                self._values["lambda_invoke_policy"] = lambda_invoke_policy
            if step_functions_execution_policy is not None:
                self._values["step_functions_execution_policy"] = step_functions_execution_policy

        @builtins.property
        def lambda_invoke_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnStateMachine.FunctionSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.LambdaInvokePolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("lambda_invoke_policy")
            return typing.cast(typing.Optional[typing.Union["CfnStateMachine.FunctionSAMPTProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def step_functions_execution_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", _IResolvable_da3f097b]]:
            '''``CfnStateMachine.SAMPolicyTemplateProperty.StepFunctionsExecutionPolicy``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("step_functions_execution_policy")
            return typing.cast(typing.Optional[typing.Union["CfnStateMachine.StateMachineSAMPTProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMPolicyTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.ScheduleEventProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule": "schedule", "input": "input"},
    )
    class ScheduleEventProperty:
        def __init__(
            self,
            *,
            schedule: builtins.str,
            input: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule: ``CfnStateMachine.ScheduleEventProperty.Schedule``.
            :param input: ``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "schedule": schedule,
            }
            if input is not None:
                self._values["input"] = input

        @builtins.property
        def schedule(self) -> builtins.str:
            '''``CfnStateMachine.ScheduleEventProperty.Schedule``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("schedule")
            assert result is not None, "Required property 'schedule' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''``CfnStateMachine.ScheduleEventProperty.Input``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#schedule
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_sam.CfnStateMachine.StateMachineSAMPTProperty",
        jsii_struct_bases=[],
        name_mapping={"state_machine_name": "stateMachineName"},
    )
    class StateMachineSAMPTProperty:
        def __init__(self, *, state_machine_name: builtins.str) -> None:
            '''
            :param state_machine_name: ``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "state_machine_name": state_machine_name,
            }

        @builtins.property
        def state_machine_name(self) -> builtins.str:
            '''``CfnStateMachine.StateMachineSAMPTProperty.StateMachineName``.

            :link: https://github.com/awslabs/serverless-application-model/blob/master/docs/policy_templates.rst
            '''
            result = self._values.get("state_machine_name")
            assert result is not None, "Required property 'state_machine_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateMachineSAMPTProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_sam.CfnStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "definition_substitutions": "definitionSubstitutions",
        "definition_uri": "definitionUri",
        "events": "events",
        "logging": "logging",
        "name": "name",
        "policies": "policies",
        "role": "role",
        "tags": "tags",
        "type": "type",
    },
)
class CfnStateMachineProps:
    def __init__(
        self,
        *,
        definition: typing.Any = None,
        definition_substitutions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        definition_uri: typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_da3f097b]] = None,
        events: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_da3f097b]]]] = None,
        logging: typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.Sequence[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Serverless::StateMachine``.

        :param definition: ``AWS::Serverless::StateMachine.Definition``.
        :param definition_substitutions: ``AWS::Serverless::StateMachine.DefinitionSubstitutions``.
        :param definition_uri: ``AWS::Serverless::StateMachine.DefinitionUri``.
        :param events: ``AWS::Serverless::StateMachine.Events``.
        :param logging: ``AWS::Serverless::StateMachine.Logging``.
        :param name: ``AWS::Serverless::StateMachine.Name``.
        :param policies: ``AWS::Serverless::StateMachine.Policies``.
        :param role: ``AWS::Serverless::StateMachine.Role``.
        :param tags: ``AWS::Serverless::StateMachine.Tags``.
        :param type: ``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if definition is not None:
            self._values["definition"] = definition
        if definition_substitutions is not None:
            self._values["definition_substitutions"] = definition_substitutions
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if events is not None:
            self._values["events"] = events
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if policies is not None:
            self._values["policies"] = policies
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def definition(self) -> typing.Any:
        '''``AWS::Serverless::StateMachine.Definition``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Any, result)

    @builtins.property
    def definition_substitutions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Serverless::StateMachine.DefinitionSubstitutions``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_substitutions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def definition_uri(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::StateMachine.DefinitionUri``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnStateMachine.S3LocationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::StateMachine.Events``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnStateMachine.EventSourceProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Serverless::StateMachine.Logging``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[CfnStateMachine.LoggingConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Name``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::Serverless::StateMachine.Policies``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, _IResolvable_da3f097b, typing.List[typing.Union[builtins.str, CfnStateMachine.IAMPolicyDocumentProperty, CfnStateMachine.SAMPolicyTemplateProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Role``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''``AWS::Serverless::StateMachine.Tags``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Serverless::StateMachine.Type``.

        :link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-statemachine.html
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApi",
    "CfnApiProps",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnFunction",
    "CfnFunctionProps",
    "CfnLayerVersion",
    "CfnLayerVersionProps",
    "CfnSimpleTable",
    "CfnSimpleTableProps",
    "CfnStateMachine",
    "CfnStateMachineProps",
]

publication.publish()

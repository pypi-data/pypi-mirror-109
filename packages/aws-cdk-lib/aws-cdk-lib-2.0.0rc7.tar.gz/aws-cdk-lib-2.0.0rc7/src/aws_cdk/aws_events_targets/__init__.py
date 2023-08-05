'''
# Event Targets for Amazon EventBridge

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes to send Amazon EventBridge to any
number of supported AWS Services. Instances of these classes should be passed
to the `rule.addTarget()` method.

Currently supported are:

* [Start a CodeBuild build](#start-a-codebuild-build)
* [Start a CodePipeline pipeline](#start-a-codepipeline-pipeline)
* Run an ECS task
* [Invoke a Lambda function](#invoke-a-lambda-function)
* [Invoke a API Gateway REST API](#invoke-a-api-gateway-rest-api)
* Publish a message to an SNS topic
* Send a message to an SQS queue
* [Start a StepFunctions state machine](#start-a-stepfunctions-state-machine)
* Queue a Batch job
* Make an AWS API call
* Put a record to a Kinesis stream
* [Log an event into a LogGroup](#log-an-event-into-a-loggroup)
* Put a record to a Kinesis Data Firehose stream
* Put an event on an EventBridge bus

See the README of the `@aws-cdk/aws-events` library for more information on
EventBridge.

## Event retry policy and using dead-letter queues

The Codebuild, CodePipeline, Lambda, StepFunctions and LogGroup targets support attaching a [dead letter queue and setting retry policies](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html). See the [lambda example](#invoke-a-lambda-function).
Use [escape hatches](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html) for the other target types.

## Invoke a Lambda function

Use the `LambdaFunction` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
triggered for every events from `aws.ec2` source. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_events as events
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_events_targets as targets
import aws_cdk as cdk


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_12_X,
    handler="index.handler",
    code=lambda_.Code.from_inline(f"exports.handler = {handler.toString()}")
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

queue = sqs.Queue(self, "Queue")

rule.add_target(targets.LambdaFunction(fn,
    dead_letter_queue=queue, # Optional: add a dead letter queue
    max_event_age=cdk.Duration.hours(2), # Otional: set the maxEventAge retry policy
    retry_attempts=2
))
```

## Log an event into a LogGroup

Use the `LogGroup` target to log your events in a CloudWatch LogGroup.

For example, the following code snippet creates an event rule with a CloudWatch LogGroup as a target.
Every events sent from the `aws.ec2` source will be sent to the CloudWatch LogGroup.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_logs as logs
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets


log_group = logs.LogGroup(self, "MyLogGroup",
    log_group_name="MyLogGroup"
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

rule.add_target(targets.CloudWatchLogGroup(log_group))
```

## Start a CodeBuild build

Use the `CodeBuildProject` target to trigger a CodeBuild project.

The code snippet below creates a CodeCommit repository that triggers a CodeBuild project
on commit to the master branch. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_codebuild as codebuild
import aws_sdk.aws_codecommit as codecommit
import aws_sdk.aws_sqs as sqs
from aws_cdk import aws_events_targets as targets


repo = codecommit.Repository(self, "MyRepo",
    repository_name="aws-cdk-codebuild-events"
)

project = codebuild.Project(self, "MyProject",
    source=codebuild.Source.code_commit(repository=repo)
)

dead_letter_queue = sqs.Queue(self, "DeadLetterQueue")

# trigger a build when a commit is pushed to the repo
on_commit_rule = repo.on_commit("OnCommit",
    target=targets.CodeBuildProject(project,
        dead_letter_queue=dead_letter_queue
    ),
    branches=["master"]
)
```

## Start a CodePipeline pipeline

Use the `CodePipeline` target to trigger a CodePipeline pipeline.

The code snippet below creates a CodePipeline pipeline that is triggered every hour

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_codepipeline as codepipeline
import aws_sdk.aws_sqs as sqs


pipeline = codepipeline.Pipeline(self, "Pipeline")

rule = events.Rule(stack, "Rule",
    schedule=events.Schedule.expression("rate(1 hour)")
)

rule.add_target(targets.CodePipeline(pipeline))
```

## Start a StepFunctions state machine

Use the `SfnStateMachine` target to trigger a State Machine.

The code snippet below creates a Simple StateMachine that is triggered every minute with a
dummy object as input.
You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html)
to the target.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_iam as iam
import aws_sdk.aws_sqs as sqs
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_events_targets as targets


rule = events.Rule(stack, "Rule",
    schedule=events.Schedule.rate(cdk.Duration.minutes(1))
)

dlq = sqs.Queue(stack, "DeadLetterQueue")

role = iam.Role(stack, "Role",
    assumed_by=iam.ServicePrincipal("events.amazonaws.com")
)
state_machine = sfn.StateMachine(stack, "SM",
    definition=sfn.Wait(stack, "Hello", time=sfn.WaitTime.duration(cdk.Duration.seconds(10))),
    role=role
)

rule.add_target(targets.SfnStateMachine(state_machine,
    input=events.RuleTargetInput.from_object(SomeParam="SomeValue"),
    dead_letter_queue=dlq
))
```

## Invoke a API Gateway REST API

Use the `ApiGateway` target to trigger a REST API.

The code snippet below creates a Api Gateway REST API that is invoked every hour.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_sdk.aws_iam as iam
import aws_sdk.aws_sqs as sqs
from aws_cdk import aws_apigateway as api
from aws_cdk import aws_events_targets as targets


rule = events.Rule(stack, "Rule",
    schedule=events.Schedule.rate(cdk.Duration.minutes(1))
)

fn = lambda_.Function(self, "MyFunc",
    handler="index.handler",
    runtime=lambda_.Runtime.NODEJS_12_X,
    code=lambda_.Code.from_inline("exports.handler = e => {}")
)

rest_api = api.LambdaRestApi(self, "MyRestAPI", handler=fn)

dlq = sqs.Queue(stack, "DeadLetterQueue")

rule.add_target(
    targets.ApiGateway(rest_api,
        path="/*/test",
        mehod="GET",
        stage="prod",
        path_parameter_values=["path-value"],
        header_parameters={
            "Header1": "header1"
        },
        query_string_parameters={
            "QueryParam1": "query-param-1"
        },
        dead_letter_queue=queue
    ))
```
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

import constructs
from .. import Duration as _Duration_4839e8c3
from ..aws_apigateway import RestApi as _RestApi_777c8238
from ..aws_codebuild import IProject as _IProject_aafae30a
from ..aws_codepipeline import IPipeline as _IPipeline_0931f838
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_acf8a799,
    SubnetSelection as _SubnetSelection_e57d76df,
)
from ..aws_ecs import (
    FargatePlatformVersion as _FargatePlatformVersion_55d8be5c,
    ICluster as _ICluster_16cddd09,
    ITaskDefinition as _ITaskDefinition_889ba4d8,
)
from ..aws_events import (
    IEventBus as _IEventBus_88d13111,
    IRule as _IRule_af9e3d28,
    IRuleTarget as _IRuleTarget_7a91f454,
    RuleTargetConfig as _RuleTargetConfig_4e70fe03,
    RuleTargetInput as _RuleTargetInput_6beca786,
)
from ..aws_iam import (
    IRole as _IRole_235f5d8e, PolicyStatement as _PolicyStatement_0fe33853
)
from ..aws_kinesis import IStream as _IStream_4e2457d2
from ..aws_kinesisfirehose import CfnDeliveryStream as _CfnDeliveryStream_8f3b1735
from ..aws_lambda import IFunction as _IFunction_6adb0ab8
from ..aws_logs import ILogGroup as _ILogGroup_3c4fa718
from ..aws_sns import ITopic as _ITopic_9eca4852
from ..aws_sqs import IQueue as _IQueue_7ed6f679
from ..aws_stepfunctions import IStateMachine as _IStateMachine_73e8d2b0


@jsii.implements(_IRuleTarget_7a91f454)
class ApiGateway(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.ApiGateway",
):
    '''(experimental) Use an API Gateway REST APIs as a target for Amazon EventBridge rules.

    :stability: experimental
    '''

    def __init__(
        self,
        rest_api: _RestApi_777c8238,
        *,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_body: typing.Optional[_RuleTargetInput_6beca786] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stage: typing.Optional[builtins.str] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param rest_api: -
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        :param header_parameters: (experimental) The headers to be set when requesting API. Default: no header parameters
        :param method: (experimental) The method for api resource invoked by the rule. Default: '*' that treated as ANY
        :param path: (experimental) The api resource invoked by the rule. We can use wildcards('*') to specify the path. In that case, an equal number of real values must be specified for pathParameterValues. Default: '/'
        :param path_parameter_values: (experimental) The path parameter values to be used to populate to wildcards("*") of requesting api path. Default: no path parameters
        :param post_body: (experimental) This will be the post request body send to the API. Default: the entire EventBridge event
        :param query_string_parameters: (experimental) The query parameters to be set when requesting API. Default: no querystring parameters
        :param stage: (experimental) The deploy stage of api gateway invoked by the rule. Default: the value of deploymentStage.stageName of target api gateway.
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        props = ApiGatewayProps(
            event_role=event_role,
            header_parameters=header_parameters,
            method=method,
            path=path,
            path_parameter_values=path_parameter_values,
            post_body=post_body,
            query_string_parameters=query_string_parameters,
            stage=stage,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(ApiGateway, self, [rest_api, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this API Gateway REST APIs as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> _RestApi_777c8238:
        '''
        :stability: experimental
        '''
        return typing.cast(_RestApi_777c8238, jsii.get(self, "restApi"))


@jsii.implements(_IRuleTarget_7a91f454)
class AwsApi(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.AwsApi",
):
    '''(experimental) Use an AWS Lambda function that makes API calls as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        policy_statement: typing.Optional[_PolicyStatement_0fe33853] = None,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param policy_statement: (experimental) The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call
        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters

        :stability: experimental
        '''
        props = AwsApiProps(
            policy_statement=policy_statement,
            action=action,
            service=service,
            api_version=api_version,
            catch_error_pattern=catch_error_pattern,
            parameters=parameters,
        )

        jsii.create(AwsApi, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this AwsApi as a result from an EventBridge event.

        :param rule: -
        :param id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.AwsApiInput",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
    },
)
class AwsApiInput:
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
    ) -> None:
        '''(experimental) Rule target input for an AwsApi target.

        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def action(self) -> builtins.str:
        '''(experimental) The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        :stability: experimental
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors

        :stability: experimental
        '''
        result = self._values.get("catch_error_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.AwsApiProps",
    jsii_struct_bases=[AwsApiInput],
    name_mapping={
        "action": "action",
        "service": "service",
        "api_version": "apiVersion",
        "catch_error_pattern": "catchErrorPattern",
        "parameters": "parameters",
        "policy_statement": "policyStatement",
    },
)
class AwsApiProps(AwsApiInput):
    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        api_version: typing.Optional[builtins.str] = None,
        catch_error_pattern: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        policy_statement: typing.Optional[_PolicyStatement_0fe33853] = None,
    ) -> None:
        '''(experimental) Properties for an AwsApi target.

        :param action: (experimental) The service action to call.
        :param service: (experimental) The service to call.
        :param api_version: (experimental) API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: (experimental) The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param parameters: (experimental) The parameters for the service action. Default: - no parameters
        :param policy_statement: (experimental) The IAM policy statement to allow the API call. Use only if resource restriction is needed. Default: - extract the permission from the API call

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if catch_error_pattern is not None:
            self._values["catch_error_pattern"] = catch_error_pattern
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy_statement is not None:
            self._values["policy_statement"] = policy_statement

    @builtins.property
    def action(self) -> builtins.str:
        '''(experimental) The service action to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(experimental) The service to call.

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) API version to use for the service.

        :default: - use latest available API version

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        :stability: experimental
        '''
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def catch_error_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        :default: - do not catch errors

        :stability: experimental
        '''
        result = self._values.get("catch_error_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''(experimental) The parameters for the service action.

        :default: - no parameters

        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_statement(self) -> typing.Optional[_PolicyStatement_0fe33853]:
        '''(experimental) The IAM policy statement to allow the API call.

        Use only if
        resource restriction is needed.

        :default: - extract the permission from the API call

        :stability: experimental
        '''
        result = self._values.get("policy_statement")
        return typing.cast(typing.Optional[_PolicyStatement_0fe33853], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class BatchJob(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.BatchJob",
):
    '''(experimental) Use an AWS Batch Job / Queue as an event rule target.

    Most likely the code will look something like this:
    ``new BatchJob(jobQueue.jobQueueArn, jobQueue, jobDefinition.jobDefinitionArn, jobDefinition)``

    In the future this API will be improved to be fully typed

    :stability: experimental
    '''

    def __init__(
        self,
        job_queue_arn: builtins.str,
        job_queue_scope: constructs.IConstruct,
        job_definition_arn: builtins.str,
        job_definition_scope: constructs.IConstruct,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param job_queue_arn: The JobQueue arn.
        :param job_queue_scope: The JobQueue Resource.
        :param job_definition_arn: The jobDefinition arn.
        :param job_definition_scope: The JobQueue Resource.
        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        '''
        props = BatchJobProps(
            attempts=attempts, event=event, job_name=job_name, size=size
        )

        jsii.create(BatchJob, self, [job_queue_arn, job_queue_scope, job_definition_arn, job_definition_scope, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger queue this batch job as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, _id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.BatchJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "attempts": "attempts",
        "event": "event",
        "job_name": "jobName",
        "size": "size",
    },
)
class BatchJobProps:
    def __init__(
        self,
        *,
        attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        job_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Customize the Batch Job Event Target.

        :param attempts: (experimental) The number of times to attempt to retry, if the job fails. Valid values are 1–10. Default: no retryStrategy is set
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param job_name: (experimental) The name of the submitted job. Default: - Automatically generated
        :param size: (experimental) The size of the array, if this is an array batch job. Valid values are integers between 2 and 10,000. Default: no arrayProperties are set

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if attempts is not None:
            self._values["attempts"] = attempts
        if event is not None:
            self._values["event"] = event
        if job_name is not None:
            self._values["job_name"] = job_name
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to attempt to retry, if the job fails.

        Valid values are 1–10.

        :default: no retryStrategy is set

        :stability: experimental
        '''
        result = self._values.get("attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the submitted job.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the array, if this is an array batch job.

        Valid values are integers between 2 and 10,000.

        :default: no arrayProperties are set

        :stability: experimental
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class CloudWatchLogGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.CloudWatchLogGroup",
):
    '''(experimental) Use an AWS CloudWatch LogGroup as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        log_group: _ILogGroup_3c4fa718,
        *,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param log_group: -
        :param event: (experimental) The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        props = LogGroupProps(
            event=event,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(CloudWatchLogGroup, self, [log_group, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to log an event into a CloudWatch LogGroup.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.implements(_IRuleTarget_7a91f454)
class CodeBuildProject(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.CodeBuildProject",
):
    '''(experimental) Start a CodeBuild build when an Amazon EventBridge rule is triggered.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _IProject_aafae30a,
        *,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param project: -
        :param event: (experimental) The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        props = CodeBuildProjectProps(
            event=event,
            event_role=event_role,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(CodeBuildProject, self, [project, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Allows using build projects as event rule targets.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.implements(_IRuleTarget_7a91f454)
class CodePipeline(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.CodePipeline",
):
    '''(experimental) Allows the pipeline to be used as an EventBridge rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        pipeline: _IPipeline_0931f838,
        *,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        options = CodePipelineTargetOptions(
            event_role=event_role,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(CodePipeline, self, [pipeline, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.ContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "memory_limit": "memoryLimit",
        "memory_reservation": "memoryReservation",
    },
)
class ContainerOverride:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.Sequence["TaskEnvironmentVariable"]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param container_name: (experimental) Name of the container inside the task definition.
        :param command: (experimental) Command to run inside the container. Default: Default command
        :param cpu: (experimental) The number of cpu units reserved for the container. Default: The default value from the task definition.
        :param environment: (experimental) Variables to set in the container's environment.
        :param memory_limit: (experimental) Hard memory limit on the container. Default: The default value from the task definition.
        :param memory_reservation: (experimental) Soft memory limit on the container. Default: The default value from the task definition.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "container_name": container_name,
        }
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) Name of the container inside the task definition.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Command to run inside the container.

        :default: Default command

        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of cpu units reserved for the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        '''(experimental) Variables to set in the container's environment.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.List["TaskEnvironmentVariable"]], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Hard memory limit on the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Soft memory limit on the container.

        :default: The default value from the task definition.

        :stability: experimental
        '''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class EcsTask(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.EcsTask",
):
    '''(experimental) Start a task on an ECS cluster.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        cluster: _ICluster_16cddd09,
        task_definition: _ITaskDefinition_889ba4d8,
        container_overrides: typing.Optional[typing.Sequence[ContainerOverride]] = None,
        platform_version: typing.Optional[_FargatePlatformVersion_55d8be5c] = None,
        role: typing.Optional[_IRole_235f5d8e] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_acf8a799]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_e57d76df] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster: (experimental) Cluster where service will be deployed.
        :param task_definition: (experimental) Task Definition of the task that should be started.
        :param container_overrides: (experimental) Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: (experimental) The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: (experimental) Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_groups: (experimental) Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: (experimental) In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: (experimental) How many tasks should be started when this event is triggered. Default: 1

        :stability: experimental
        '''
        props = EcsTaskProps(
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            platform_version=platform_version,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            task_count=task_count,
        )

        jsii.create(EcsTask, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Allows using tasks as target of EventBridge events.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_acf8a799]]:
        '''(experimental) The security groups associated with the task.

        Only applicable with awsvpc network mode.

        :default: - A new security group is created.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_acf8a799]], jsii.get(self, "securityGroups"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.EcsTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "platform_version": "platformVersion",
        "role": "role",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "task_count": "taskCount",
    },
)
class EcsTaskProps:
    def __init__(
        self,
        *,
        cluster: _ICluster_16cddd09,
        task_definition: _ITaskDefinition_889ba4d8,
        container_overrides: typing.Optional[typing.Sequence[ContainerOverride]] = None,
        platform_version: typing.Optional[_FargatePlatformVersion_55d8be5c] = None,
        role: typing.Optional[_IRole_235f5d8e] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_acf8a799]] = None,
        subnet_selection: typing.Optional[_SubnetSelection_e57d76df] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties to define an ECS Event Task.

        :param cluster: (experimental) Cluster where service will be deployed.
        :param task_definition: (experimental) Task Definition of the task that should be started.
        :param container_overrides: (experimental) Container setting overrides. Key is the name of the container to override, value is the values you want to override.
        :param platform_version: (experimental) The platform version on which to run your task. Unless you have specific compatibility requirements, you don't need to specify this. Default: - ECS will set the Fargate platform version to 'LATEST'
        :param role: (experimental) Existing IAM role to run the ECS task. Default: A new IAM role is created
        :param security_groups: (experimental) Existing security groups to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnet_selection: (experimental) In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param task_count: (experimental) How many tasks should be started when this event is triggered. Default: 1

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_e57d76df(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def cluster(self) -> _ICluster_16cddd09:
        '''(experimental) Cluster where service will be deployed.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_ICluster_16cddd09, result)

    @builtins.property
    def task_definition(self) -> _ITaskDefinition_889ba4d8:
        '''(experimental) Task Definition of the task that should be started.

        :stability: experimental
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_ITaskDefinition_889ba4d8, result)

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        '''(experimental) Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :stability: experimental
        '''
        result = self._values.get("container_overrides")
        return typing.cast(typing.Optional[typing.List[ContainerOverride]], result)

    @builtins.property
    def platform_version(self) -> typing.Optional[_FargatePlatformVersion_55d8be5c]:
        '''(experimental) The platform version on which to run your task.

        Unless you have specific compatibility requirements, you don't need to specify this.

        :default: - ECS will set the Fargate platform version to 'LATEST'

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
        :stability: experimental
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_FargatePlatformVersion_55d8be5c], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) Existing IAM role to run the ECS task.

        :default: A new IAM role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_acf8a799]]:
        '''(experimental) Existing security groups to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_acf8a799]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_e57d76df]:
        '''(experimental) In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_e57d76df], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many tasks should be started when this event is triggered.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class EventBus(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.EventBus",
):
    '''(experimental) Notify an existing Event Bus of an event.

    :stability: experimental
    '''

    def __init__(
        self,
        event_bus: _IEventBus_88d13111,
        *,
        role: typing.Optional[_IRole_235f5d8e] = None,
    ) -> None:
        '''
        :param event_bus: -
        :param role: (experimental) Role to be used to publish the event. Default: a new role is created.

        :stability: experimental
        '''
        props = EventBusProps(role=role)

        jsii.create(EventBus, self, [event_bus, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns the rule target specification.

        NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        :param rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, _id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.EventBusProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class EventBusProps:
    def __init__(self, *, role: typing.Optional[_IRole_235f5d8e] = None) -> None:
        '''(experimental) Configuration properties of an Event Bus event.

        :param role: (experimental) Role to be used to publish the event. Default: a new role is created.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) Role to be used to publish the event.

        :default: a new role is created.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBusProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class KinesisFirehoseStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.KinesisFirehoseStream",
):
    '''(experimental) Customize the Firehose Stream Event Target.

    :stability: experimental
    '''

    def __init__(
        self,
        stream: _CfnDeliveryStream_8f3b1735,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''
        :param stream: -
        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event

        :stability: experimental
        '''
        props = KinesisFirehoseStreamProps(message=message)

        jsii.create(KinesisFirehoseStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Firehose Stream as a result from a Event Bridge event.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.KinesisFirehoseStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class KinesisFirehoseStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''(experimental) Customize the Firehose Stream Event Target.

        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire Event Bridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire Event Bridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisFirehoseStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class KinesisStream(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.KinesisStream",
):
    '''(experimental) Use a Kinesis Stream as a target for AWS CloudWatch event rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # put to a Kinesis stream every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.KinesisStream(stream))
    '''

    def __init__(
        self,
        stream: _IStream_4e2457d2,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param stream: -
        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: (experimental) Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        :stability: experimental
        '''
        props = KinesisStreamProps(
            message=message, partition_key_path=partition_key_path
        )

        jsii.create(KinesisStream, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Kinesis Stream as a result from a CloudWatch event.

        :param _rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.KinesisStreamProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "partition_key_path": "partitionKeyPath"},
)
class KinesisStreamProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
        partition_key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Customize the Kinesis Stream Event Target.

        :param message: (experimental) The message to send to the stream. Must be a valid JSON text passed to the target stream. Default: - the entire CloudWatch event
        :param partition_key_path: (experimental) Partition Key Path for records sent to this stream. Default: - eventId as the partition key

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if partition_key_path is not None:
            self._values["partition_key_path"] = partition_key_path

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The message to send to the stream.

        Must be a valid JSON text passed to the target stream.

        :default: - the entire CloudWatch event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def partition_key_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Partition Key Path for records sent to this stream.

        :default: - eventId as the partition key

        :stability: experimental
        '''
        result = self._values.get("partition_key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class LambdaFunction(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.LambdaFunction",
):
    '''(experimental) Use an AWS Lambda function as an event rule target.

    :stability: experimental
    '''

    def __init__(
        self,
        handler: _IFunction_6adb0ab8,
        *,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param handler: -
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        props = LambdaFunctionProps(
            event=event,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(LambdaFunction, self, [handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this Lambda as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, _id]))


@jsii.implements(_IRuleTarget_7a91f454)
class SfnStateMachine(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.SfnStateMachine",
):
    '''(experimental) Use a StepFunctions state machine as a target for Amazon EventBridge rules.

    :stability: experimental
    '''

    def __init__(
        self,
        machine: _IStateMachine_73e8d2b0,
        *,
        input: typing.Optional[_RuleTargetInput_6beca786] = None,
        role: typing.Optional[_IRole_235f5d8e] = None,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine: -
        :param input: (experimental) The input to the state machine execution. Default: the entire EventBridge event
        :param role: (experimental) The IAM role to be assumed to execute the State Machine. Default: - a new role will be created
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        props = SfnStateMachineProps(
            input=input,
            role=role,
            dead_letter_queue=dead_letter_queue,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
        )

        jsii.create(SfnStateMachine, self, [machine, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a properties that are used in an Rule to trigger this State Machine.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="machine")
    def machine(self) -> _IStateMachine_73e8d2b0:
        '''
        :stability: experimental
        '''
        return typing.cast(_IStateMachine_73e8d2b0, jsii.get(self, "machine"))


@jsii.implements(_IRuleTarget_7a91f454)
class SnsTopic(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.SnsTopic",
):
    '''(experimental) Use an SNS topic as a target for Amazon EventBridge rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SNS topic every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SnsTopic(topic))
    '''

    def __init__(
        self,
        topic: _ITopic_9eca4852,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''
        :param topic: -
        :param message: (experimental) The message to send to the topic. Default: the entire EventBridge event

        :stability: experimental
        '''
        props = SnsTopicProps(message=message)

        jsii.create(SnsTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this SNS topic as a result from an EventBridge event.

        :param _rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sns-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [_rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_9eca4852:
        '''
        :stability: experimental
        '''
        return typing.cast(_ITopic_9eca4852, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.SnsTopicProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message"},
)
class SnsTopicProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''(experimental) Customize the SNS Topic Event Target.

        :param message: (experimental) The message to send to the topic. Default: the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The message to send to the topic.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IRuleTarget_7a91f454)
class SqsQueue(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_events_targets.SqsQueue",
):
    '''(experimental) Use an SQS Queue as a target for Amazon EventBridge rules.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        # publish to an SQS queue every time code is committed
        # to a CodeCommit repository
        repository.on_commit(targets.SqsQueue(queue))
    '''

    def __init__(
        self,
        queue: _IQueue_7ed6f679,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param queue: -
        :param message: (experimental) The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: (experimental) Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        :stability: experimental
        '''
        props = SqsQueueProps(message=message, message_group_id=message_group_id)

        jsii.create(SqsQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        rule: _IRule_af9e3d28,
        _id: typing.Optional[builtins.str] = None,
    ) -> _RuleTargetConfig_4e70fe03:
        '''(experimental) Returns a RuleTarget that can be used to trigger this SQS queue as a result from an EventBridge event.

        :param rule: -
        :param _id: -

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/resource-based-policies-eventbridge.html#sqs-permissions
        :stability: experimental
        '''
        return typing.cast(_RuleTargetConfig_4e70fe03, jsii.invoke(self, "bind", [rule, _id]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_7ed6f679:
        '''
        :stability: experimental
        '''
        return typing.cast(_IQueue_7ed6f679, jsii.get(self, "queue"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.SqsQueueProps",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "message_group_id": "messageGroupId"},
)
class SqsQueueProps:
    def __init__(
        self,
        *,
        message: typing.Optional[_RuleTargetInput_6beca786] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Customize the SQS Queue Event Target.

        :param message: (experimental) The message to send to the queue. Must be a valid JSON text passed to the target queue. Default: the entire EventBridge event
        :param message_group_id: (experimental) Message Group ID for messages sent to this queue. Required for FIFO queues, leave empty for regular queues. Default: - no message group ID (regular queue)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The message to send to the queue.

        Must be a valid JSON text passed to the target queue.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Message Group ID for messages sent to this queue.

        Required for FIFO queues, leave empty for regular queues.

        :default: - no message group ID (regular queue)

        :stability: experimental
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.TargetBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
    },
)
class TargetBaseProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The generic properties for an RuleTarget.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.TaskEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class TaskEnvironmentVariable:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) An environment variable to be set in the container run as a task.

        :param name: (experimental) Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: (experimental) Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.ApiGatewayProps",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "event_role": "eventRole",
        "header_parameters": "headerParameters",
        "method": "method",
        "path": "path",
        "path_parameter_values": "pathParameterValues",
        "post_body": "postBody",
        "query_string_parameters": "queryStringParameters",
        "stage": "stage",
    },
)
class ApiGatewayProps(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_body: typing.Optional[_RuleTargetInput_6beca786] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Customize the API Gateway Event Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created
        :param header_parameters: (experimental) The headers to be set when requesting API. Default: no header parameters
        :param method: (experimental) The method for api resource invoked by the rule. Default: '*' that treated as ANY
        :param path: (experimental) The api resource invoked by the rule. We can use wildcards('*') to specify the path. In that case, an equal number of real values must be specified for pathParameterValues. Default: '/'
        :param path_parameter_values: (experimental) The path parameter values to be used to populate to wildcards("*") of requesting api path. Default: no path parameters
        :param post_body: (experimental) This will be the post request body send to the API. Default: the entire EventBridge event
        :param query_string_parameters: (experimental) The query parameters to be set when requesting API. Default: no querystring parameters
        :param stage: (experimental) The deploy stage of api gateway invoked by the rule. Default: the value of deploymentStage.stageName of target api gateway.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if event_role is not None:
            self._values["event_role"] = event_role
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if post_body is not None:
            self._values["post_body"] = post_body
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The headers to be set when requesting API.

        :default: no header parameters

        :stability: experimental
        '''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''(experimental) The method for api resource invoked by the rule.

        :default: '*' that treated as ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The api resource invoked by the rule.

        We can use wildcards('*') to specify the path. In that case,
        an equal number of real values must be specified for pathParameterValues.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The path parameter values to be used to populate to wildcards("*") of requesting api path.

        :default: no path parameters

        :stability: experimental
        '''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def post_body(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) This will be the post request body send to the API.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("post_body")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The query parameters to be set when requesting API.

        :default: no querystring parameters

        :stability: experimental
        '''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) The deploy stage of api gateway invoked by the rule.

        :default: the value of deploymentStage.stageName of target api gateway.

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.CodeBuildProjectProps",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "event": "event",
        "event_role": "eventRole",
    },
)
class CodeBuildProjectProps(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
    ) -> None:
        '''(experimental) Customize the CodeBuild Event Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param event: (experimental) The event to send to CodeBuild. This will be the payload for the StartBuild API. Default: - the entire EventBridge event
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if event is not None:
            self._values["event"] = event
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The event to send to CodeBuild.

        This will be the payload for the StartBuild API.

        :default: - the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) The role to assume before invoking the target (i.e., the codebuild) when the given rule is triggered.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.CodePipelineTargetOptions",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "event_role": "eventRole",
    },
)
class CodePipelineTargetOptions(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        event_role: typing.Optional[_IRole_235f5d8e] = None,
    ) -> None:
        '''(experimental) Customization options when creating a {@link CodePipeline} event target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param event_role: (experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if event_role is not None:
            self._values["event_role"] = event_role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) The role to assume before invoking the target (i.e., the pipeline) when the given rule is triggered.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.LambdaFunctionProps",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "event": "event",
    },
)
class LambdaFunctionProps(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''(experimental) Customize the Lambda Event Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param event: (experimental) The event to send to the Lambda. This will be the payload sent to the Lambda Function. Default: the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The event to send to the Lambda.

        This will be the payload sent to the Lambda Function.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.LogGroupProps",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "event": "event",
    },
)
class LogGroupProps(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        event: typing.Optional[_RuleTargetInput_6beca786] = None,
    ) -> None:
        '''(experimental) Customize the CloudWatch LogGroup Event Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param event: (experimental) The event to send to the CloudWatch LogGroup. This will be the event logged into the CloudWatch LogGroup Default: - the entire EventBridge event

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if event is not None:
            self._values["event"] = event

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def event(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The event to send to the CloudWatch LogGroup.

        This will be the event logged into the CloudWatch LogGroup

        :default: - the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_events_targets.SfnStateMachineProps",
    jsii_struct_bases=[TargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "input": "input",
        "role": "role",
    },
)
class SfnStateMachineProps(TargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_7ed6f679] = None,
        max_event_age: typing.Optional[_Duration_4839e8c3] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        input: typing.Optional[_RuleTargetInput_6beca786] = None,
        role: typing.Optional[_IRole_235f5d8e] = None,
    ) -> None:
        '''(experimental) Customize the Step Functions State Machine target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param input: (experimental) The input to the state machine execution. Default: the entire EventBridge event
        :param role: (experimental) The IAM role to be assumed to execute the State Machine. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if input is not None:
            self._values["input"] = input
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_7ed6f679]:
        '''(experimental) The SQS queue to be used as deadLetterQueue. Check out the `considerations for using a dead-letter queue <https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html#dlq-considerations>`_.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_7ed6f679], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def input(self) -> typing.Optional[_RuleTargetInput_6beca786]:
        '''(experimental) The input to the state machine execution.

        :default: the entire EventBridge event

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_RuleTargetInput_6beca786], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_235f5d8e]:
        '''(experimental) The IAM role to be assumed to execute the State Machine.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_235f5d8e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiGateway",
    "ApiGatewayProps",
    "AwsApi",
    "AwsApiInput",
    "AwsApiProps",
    "BatchJob",
    "BatchJobProps",
    "CloudWatchLogGroup",
    "CodeBuildProject",
    "CodeBuildProjectProps",
    "CodePipeline",
    "CodePipelineTargetOptions",
    "ContainerOverride",
    "EcsTask",
    "EcsTaskProps",
    "EventBus",
    "EventBusProps",
    "KinesisFirehoseStream",
    "KinesisFirehoseStreamProps",
    "KinesisStream",
    "KinesisStreamProps",
    "LambdaFunction",
    "LambdaFunctionProps",
    "LogGroupProps",
    "SfnStateMachine",
    "SfnStateMachineProps",
    "SnsTopic",
    "SnsTopicProps",
    "SqsQueue",
    "SqsQueueProps",
    "TargetBaseProps",
    "TaskEnvironmentVariable",
]

publication.publish()

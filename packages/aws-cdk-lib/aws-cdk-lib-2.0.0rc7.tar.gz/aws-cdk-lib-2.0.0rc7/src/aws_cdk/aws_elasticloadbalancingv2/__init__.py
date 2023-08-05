'''
# Amazon Elastic Load Balancing V2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

The `@aws-cdk/aws-elasticloadbalancingv2` package provides constructs for
configuring application and network load balancers.

For more information, see the AWS documentation for
[Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)
and [Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html).

## Defining an Application Load Balancer

You define an application load balancer by creating an instance of
`ApplicationLoadBalancer`, adding a Listener to the load balancer
and adding Targets to the Listener:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk_lib.aws_autoscaling import AutoScalingGroup


# ...

vpc = ec2.Vpc(...)

# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener and open up the load balancer's security group
# to the world.
listener = lb.add_listener("Listener",
    port=80,

    # 'open: true' is the default, you can leave it out if you want. Set it
    # to 'false' and use `listener.connections` if you want to be selective
    # about who can access the load balancer.
    open=True
)

# Create an AutoScaling group and add it as a load balancing
# target to the listener.
asg = AutoScalingGroup(...)
listener.add_targets("ApplicationFleet",
    port=8080,
    targets=[asg]
)
```

The security groups of the load balancer and the target are automatically
updated to allow the network traffic.

One (or more) security groups can be associated with the load balancer;
if a security group isn't provided, one will be automatically created.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
security_group1 = ec2.SecurityGroup(stack, "SecurityGroup1", vpc=vpc)
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True,
    security_group=security_group1
)

security_group2 = ec2.SecurityGroup(stack, "SecurityGroup2", vpc=vpc)
lb.add_security_group(security_group2)
```

### Conditions

It's possible to route traffic to targets based on conditions in the incoming
HTTP request. For example, the following will route requests to the indicated
AutoScalingGroup only if the requested host in the request is either for
`example.com/ok` or `example.com/path`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("Example.Com Fleet",
    priority=10,
    conditions=[
        ListenerCondition.host_headers(["example.com"]),
        ListenerCondition.path_patterns(["/ok", "/path"])
    ],
    port=8080,
    targets=[asg]
)
```

A target with a condition contains either `pathPatterns` or `hostHeader`, or
both. If both are specified, both conditions must be met for the requests to
be routed to the given target. `priority` is a required field when you add
targets with conditions. The lowest number wins.

Every listener must have at least one target without conditions, which is
where all requests that didn't match any of the conditions will be sent.

### Convenience methods and more complex Actions

Routing traffic from a Load Balancer to a Target involves the following steps:

* Create a Target Group, register the Target into the Target Group
* Add an Action to the Listener which forwards traffic to the Target Group.

Various methods on the `Listener` take care of this work for you to a greater
or lesser extent:

* `addTargets()` performs both steps: automatically creates a Target Group and the
  required Action.
* `addTargetGroups()` gives you more control: you create the Target Group (or
  Target Groups) yourself and the method creates Action that routes traffic to
  the Target Groups.
* `addAction()` gives you full control: you supply the Action and wire it up
  to the Target Groups yourself (or access one of the other ELB routing features).

Using `addAction()` gives you access to some of the features of an Elastic Load
Balancer that the other two convenience methods don't:

* **Routing stickiness**: use `ListenerAction.forward()` and supply a
  `stickinessDuration` to make sure requests are routed to the same target group
  for a given duration.
* **Weighted Target Groups**: use `ListenerAction.weightedForward()`
  to give different weights to different target groups.
* **Fixed Responses**: use `ListenerAction.fixedResponse()` to serve
  a static response (ALB only).
* **Redirects**: use `ListenerAction.redirect()` to serve an HTTP
  redirect response (ALB only).
* **Authentication**: use `ListenerAction.authenticateOidc()` to
  perform OpenID authentication before serving a request (see the
  `@aws-cdk/aws-elasticloadbalancingv2-actions` package for direct authentication
  integration with Cognito) (ALB only).

Here's an example of serving a fixed response at the `/ok` URL:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_action("Fixed",
    priority=10,
    conditions=[
        ListenerCondition.path_patterns(["/ok"])
    ],
    action=ListenerAction.fixed_response(200,
        content_type=elbv2.ContentType.TEXT_PLAIN,
        message_body="OK"
    )
)
```

Here's an example of using OIDC authentication before forwarding to a TargetGroup:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_action("DefaultAction",
    action=ListenerAction.authenticate_oidc(
        authorization_endpoint="https://example.com/openid",
        # Other OIDC properties here
        # ...
        next=ListenerAction.forward([my_target_group])
    )
)
```

If you just want to redirect all incoming traffic on one port to another port, you can use the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lb.add_redirect(
    source_protocol=elbv2.ApplicationProtocol.HTTPS,
    source_port=8443,
    target_protocol=elbv2.ApplicationProtocol.HTTP,
    target_port=8080
)
```

If you do not provide any options for this method, it redirects HTTP port 80 to HTTPS port 443.

By default all ingress traffic will be allowed on the source port. If you want to be more selective with your
ingress rules then set `open: false` and use the listener's `connections` object to selectively grant access to the listener.

## Defining a Network Load Balancer

Network Load Balancers are defined in a similar way to Application Load
Balancers:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_autoscaling as autoscaling


# Create the load balancer in a VPC. 'internetFacing' is 'false'
# by default, which creates an internal load balancer.
lb = elbv2.NetworkLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)

# Add a listener on a particular port.
listener = lb.add_listener("Listener",
    port=443
)

# Add targets on a particular port.
listener.add_targets("AppFleet",
    port=443,
    targets=[asg]
)
```

One thing to keep in mind is that network load balancers do not have security
groups, and no automatic security group configuration is done for you. You will
have to configure the security groups of the target yourself to allow traffic by
clients and/or load balancer instances, depending on your target types.  See
[Target Groups for your Network Load
Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-target-groups.html)
and [Register targets with your Target
Group](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html)
for more information.

## Targets and Target Groups

Application and Network Load Balancers organize load balancing targets in Target
Groups. If you add your balancing targets (such as AutoScalingGroups, ECS
services or individual instances) to your listener directly, the appropriate
`TargetGroup` will be automatically created for you.

If you need more control over the Target Groups created, create an instance of
`ApplicationTargetGroup` or `NetworkTargetGroup`, add the members you desire,
and add it to the listener by calling `addTargetGroups` instead of `addTargets`.

`addTargets()` will always return the Target Group it just created for you:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
group = listener.add_targets("AppFleet",
    port=443,
    targets=[asg1]
)

group.add_target(asg2)
```

### Sticky sessions for your Application Load Balancer

By default, an Application Load Balancer routes each request independently to a registered target based on the chosen load-balancing algorithm. However, you can use the sticky session feature (also known as session affinity) to enable the load balancer to bind a user's session to a specific target. This ensures that all requests from the user during the session are sent to the same target. This feature is useful for servers that maintain state information in order to provide a continuous experience to clients. To use sticky sessions, the client must support cookies.

Application Load Balancers support both duration-based cookies (`lb_cookie`) and application-based cookies (`app_cookie`). The key to managing sticky sessions is determining how long your load balancer should consistently route the user's request to the same target. Sticky sessions are enabled at the target group level. You can use a combination of duration-based stickiness, application-based stickiness, and no stickiness across all of your target groups.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Target group with duration-based stickiness with load-balancer generated cookie
tg1 = elbv2.ApplicationTargetGroup(stack, "TG1",
    target_type=elbv2.TargetType.INSTANCE,
    port=80,
    stickiness_cookie_duration=cdk.Duration.minutes(5),
    vpc=vpc
)

# Target group with application-based stickiness
tg2 = elbv2.ApplicationTargetGroup(stack, "TG2",
    target_type=elbv2.TargetType.INSTANCE,
    port=80,
    stickiness_cookie_duration=cdk.Duration.minutes(5),
    stickiness_cookie_name="MyDeliciousCookie",
    vpc=vpc
)
```

For more information see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html#application-based-stickiness

### Setting the target group protocol version

By default, Application Load Balancers send requests to targets using HTTP/1.1. You can use the [protocol version](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-protocol-version) to send requests to targets using HTTP/2 or gRPC.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tg = elbv2.ApplicationTargetGroup(stack, "TG",
    target_type=elbv2.TargetType.IP,
    port=50051,
    protocol=elbv2.ApplicationProtocol.HTTP,
    protocol_version=elbv2.ApplicationProtocolVersion.GRPC,
    health_check={
        "enabled": True,
        "healthy_grpc_codes": "0-99"
    },
    vpc=vpc
)
```

## Using Lambda Targets

To use a Lambda Function as a target, use the integration class in the
`@aws-cdk/aws-elasticloadbalancingv2-targets` package:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_elasticloadbalancingv2_targets as targets


lambda_function = lambda_.Function(...)
lb = elbv2.ApplicationLoadBalancer(...)

listener = lb.add_listener("Listener", port=80)
listener.add_targets("Targets",
    targets=[targets.LambdaTarget(lambda_function)],

    # For Lambda Targets, you need to explicitly enable health checks if you
    # want them.
    health_check=HealthCheck(
        enabled=True
    )
)
```

Only a single Lambda function can be added to a single listener rule.

## Configuring Health Checks

Health checks are configured upon creation of a target group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "path": "/ping",
        "interval": cdk.Duration.minutes(1)
    }
)
```

The health check can also be configured after creation by calling
`configureHealthCheck()` on the created object.

No attempts are made to configure security groups for the port you're
configuring a health check for, but if the health check is on the same port
you're routing traffic to, the security group already allows the traffic.
If not, you will have to configure the security groups appropriately:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener.add_targets("AppFleet",
    port=8080,
    targets=[asg],
    health_check={
        "port": 8088
    }
)

listener.connections.allow_from(lb, ec2.Port.tcp(8088))
```

## Using a Load Balancer from a different Stack

If you want to put your Load Balancer and the Targets it is load balancing to in
different stacks, you may not be able to use the convenience methods
`loadBalancer.addListener()` and `listener.addTargets()`.

The reason is that these methods will create resources in the same Stack as the
object they're called on, which may lead to cyclic references between stacks.
Instead, you will have to create an `ApplicationListener` in the target stack,
or an empty `TargetGroup` in the load balancer stack that you attach your
service to.

For an example of the alternatives while load balancing to an ECS service, see the
[ecs/cross-stack-load-balancer
example](https://github.com/aws-samples/aws-cdk-examples/tree/master/typescript/ecs/cross-stack-load-balancer/).

## Protocol for Load Balancer Targets

Constructs that want to be a load balancer target should implement
`IApplicationLoadBalancerTarget` and/or `INetworkLoadBalancerTarget`, and
provide an implementation for the function `attachToXxxTargetGroup()`, which can
call functions on the load balancer and should return metadata about the
load balancing target:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
attach_to_application_target_group(target_group, ApplicationTargetGroup)LoadBalancerTargetProps
    target_group.register_connectable(...)return {
        "target_type": TargetType.Instance | TargetType.Ip,
        "target_json": {"id": , ..., "port": , ...}
    }
```

`targetType` should be one of `Instance` or `Ip`. If the target can be
directly added to the target group, `targetJson` should contain the `id` of
the target (either instance ID or IP address depending on the type) and
optionally a `port` or `availabilityZone` override.

Application load balancer targets can call `registerConnectable()` on the
target group to register themselves for addition to the load balancer's security
group rules.

If your load balancer target requires that the TargetGroup has been
associated with a LoadBalancer before registration can happen (such as is the
case for ECS Services for example), take a resource dependency on
`targetGroup.loadBalancerDependency()` as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Make sure that the listener has been created, and so the TargetGroup
# has been associated with the LoadBalancer, before 'resource' is created.
resourced.add_dependency(target_group.load_balancer_dependency())
```

## Looking up Load Balancers and Listeners

You may look up load balancers and load balancer listeners by using one of the
following lookup methods:

* `ApplicationLoadBalancer.fromlookup(options)` - Look up an application load
  balancer.
* `ApplicationListener.fromLookup(options)` - Look up an application load
  balancer listener.
* `NetworkLoadBalancer.fromLookup(options)` - Look up a network load balancer.
* `NetworkListener.fromLookup(options)` - Look up a network load balancer
  listener.

### Load Balancer lookup options

You may look up a load balancer by ARN or by associated tags. When you look a
load balancer up by ARN, that load balancer will be returned unless CDK detects
that the load balancer is of the wrong type. When you look up a load balancer by
tags, CDK will return the load balancer matching all specified tags. If more
than one load balancer matches, CDK will throw an error requesting that you
provide more specific criteria.

**Look up a Application Load Balancer by ARN**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balancer = ApplicationLoadBalancer.from_lookup(stack, "ALB",
    load_balancer_arn=YOUR_ALB_ARN
)
```

**Look up an Application Load Balancer by tags**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balancer = ApplicationLoadBalancer.from_lookup(stack, "ALB",
    load_balancer_tags={
        # Finds a load balancer matching all tags.
        "some": "tag",
        "someother": "tag"
    }
)
```

## Load Balancer Listener lookup options

You may look up a load balancer listener by the following criteria:

* Associated load balancer ARN
* Associated load balancer tags
* Listener ARN
* Listener port
* Listener protocol

The lookup method will return the matching listener. If more than one listener
matches, CDK will throw an error requesting that you specify additional
criteria.

**Look up a Listener by associated Load Balancer, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = ApplicationListener.from_lookup(stack, "ALBListener",
    load_balancer_arn=YOUR_ALB_ARN,
    listener_protocol=ApplicationProtocol.HTTPS,
    listener_port=443
)
```

**Look up a Listener by associated Load Balancer Tag, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = ApplicationListener.from_lookup(stack, "ALBListener",
    load_balancer_tags={
        "Cluster": "MyClusterName"
    },
    listener_protocol=ApplicationProtocol.HTTPS,
    listener_port=443
)
```

**Look up a Network Listener by associated Load Balancer Tag, Port, and Protocol**

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
listener = NetworkListener.from_lookup(stack, "ALBListener",
    load_balancer_tags={
        "Cluster": "MyClusterName"
    },
    listener_protocol=Protocol.TCP,
    listener_port=12345
)
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
from .. import (
    CfnResource as _CfnResource_9df397a6,
    CfnTag as _CfnTag_f6864754,
    Duration as _Duration_4839e8c3,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    IResource as _IResource_c80c4260,
    Resource as _Resource_45bc6135,
    SecretValue as _SecretValue_3dd0ddae,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)
from ..aws_certificatemanager import ICertificate as _ICertificate_c194c70b
from ..aws_cloudwatch import (
    Metric as _Metric_e396a4dc,
    MetricOptions as _MetricOptions_1788b62f,
    Unit as _Unit_61bc6f70,
)
from ..aws_ec2 import (
    Connections as _Connections_0f31fce8,
    IConnectable as _IConnectable_10015a05,
    ISecurityGroup as _ISecurityGroup_acf8a799,
    IVpc as _IVpc_f30d5663,
    IVpcEndpointServiceLoadBalancer as _IVpcEndpointServiceLoadBalancer_34cbc6e3,
    Port as _Port_85922693,
    SubnetSelection as _SubnetSelection_e57d76df,
)
from ..aws_s3 import IBucket as _IBucket_42e086fd


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddNetworkActionProps",
    jsii_struct_bases=[],
    name_mapping={"action": "action"},
)
class AddNetworkActionProps:
    def __init__(self, *, action: "NetworkListenerAction") -> None:
        '''(experimental) Properties for adding a new action to a listener.

        :param action: (experimental) Action to perform.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
        }

    @builtins.property
    def action(self) -> "NetworkListenerAction":
        '''(experimental) Action to perform.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("NetworkListenerAction", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddNetworkActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddNetworkTargetsProps",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "preserve_client_ip": "preserveClientIp",
        "protocol": "protocol",
        "proxy_protocol_v2": "proxyProtocolV2",
        "target_group_name": "targetGroupName",
        "targets": "targets",
    },
)
class AddNetworkTargetsProps:
    def __init__(
        self,
        *,
        port: jsii.Number,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence["INetworkLoadBalancerTarget"]] = None,
    ) -> None:
        '''(experimental) Properties for adding new network targets to a listener.

        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param preserve_client_ip: (experimental) Indicates whether client IP preservation is enabled. Default: false if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, true.
        :param protocol: (experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - inherits the protocol of the listener
        :param proxy_protocol_v2: (experimental) Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if preserve_client_ip is not None:
            self._values["preserve_client_ip"] = preserve_client_ip
        if protocol is not None:
            self._values["protocol"] = protocol
        if proxy_protocol_v2 is not None:
            self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The port on which the listener listens for requests.

        :default: Determined from protocol if known

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        '''(experimental) Health check configuration.

        :default: No health check

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheck"], result)

    @builtins.property
    def preserve_client_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether client IP preservation is enabled.

        :default:

        false if the target group type is IP address and the
        target group protocol is TCP or TLS. Otherwise, true.

        :stability: experimental
        '''
        result = self._values.get("preserve_client_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - inherits the protocol of the listener

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether Proxy Protocol version 2 is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("proxy_protocol_v2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List["INetworkLoadBalancerTarget"]]:
        '''(experimental) The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List["INetworkLoadBalancerTarget"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddNetworkTargetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddRuleProps",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "priority": "priority"},
)
class AddRuleProps:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for adding a conditional load balancing rule.

        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List["ListenerCondition"]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List["ListenerCondition"]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "listener_arn": "listenerArn",
        "default_port": "defaultPort",
        "security_group": "securityGroup",
    },
)
class ApplicationListenerAttributes:
    def __init__(
        self,
        *,
        listener_arn: builtins.str,
        default_port: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_ISecurityGroup_acf8a799] = None,
    ) -> None:
        '''(experimental) Properties to reference an existing listener.

        :param listener_arn: (experimental) ARN of the listener.
        :param default_port: (experimental) The default port on which this listener is listening.
        :param security_group: (experimental) Security group of the load balancer this listener is associated with.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener_arn": listener_arn,
        }
        if default_port is not None:
            self._values["default_port"] = default_port
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''(experimental) ARN of the listener.

        :stability: experimental
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The default port on which this listener is listening.

        :stability: experimental
        '''
        result = self._values.get("default_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_acf8a799]:
        '''(experimental) Security group of the load balancer this listener is associated with.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_acf8a799], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationListenerCertificate(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerCertificate",
):
    '''(experimental) Add certificates to a listener.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: "IApplicationListener",
        certificates: typing.Optional[typing.Sequence["IListenerCertificate"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param listener: (experimental) The listener to attach the rule to.
        :param certificates: (experimental) Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.

        :stability: experimental
        '''
        props = ApplicationListenerCertificateProps(
            listener=listener, certificates=certificates
        )

        jsii.create(ApplicationListenerCertificate, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={"listener": "listener", "certificates": "certificates"},
)
class ApplicationListenerCertificateProps:
    def __init__(
        self,
        *,
        listener: "IApplicationListener",
        certificates: typing.Optional[typing.Sequence["IListenerCertificate"]] = None,
    ) -> None:
        '''(experimental) Properties for adding a set of certificates to a listener.

        :param listener: (experimental) The listener to attach the rule to.
        :param certificates: (experimental) Certificates to attach. Duplicates are not allowed. Default: - One of 'certificates' and 'certificateArns' is required.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if certificates is not None:
            self._values["certificates"] = certificates

    @builtins.property
    def listener(self) -> "IApplicationListener":
        '''(experimental) The listener to attach the rule to.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast("IApplicationListener", result)

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        '''(experimental) Certificates to attach.

        Duplicates are not allowed.

        :default: - One of 'certificates' and 'certificateArns' is required.

        :stability: experimental
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List["IListenerCertificate"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationListenerRule(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerRule",
):
    '''(experimental) Define a new listener rule.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: "IApplicationListener",
        priority: jsii.Number,
        action: typing.Optional["ListenerAction"] = None,
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param listener: (experimental) The listener to attach the rule to.
        :param priority: (experimental) Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: (experimental) Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param target_groups: (experimental) Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.

        :stability: experimental
        '''
        props = ApplicationListenerRuleProps(
            listener=listener,
            priority=priority,
            action=action,
            conditions=conditions,
            target_groups=target_groups,
        )

        jsii.create(ApplicationListenerRule, self, [scope, id, props])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, condition: "ListenerCondition") -> None:
        '''(experimental) Add a non-standard condition to this rule.

        :param condition: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addCondition", [condition]))

    @jsii.member(jsii_name="configureAction")
    def configure_action(self, action: "ListenerAction") -> None:
        '''(experimental) Configure the action to perform for this rule.

        :param action: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "configureAction", [action]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerRuleArn")
    def listener_rule_arn(self) -> builtins.str:
        '''(experimental) The ARN of this rule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerRuleArn"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "security_group_id": "securityGroupId",
        "load_balancer_canonical_hosted_zone_id": "loadBalancerCanonicalHostedZoneId",
        "load_balancer_dns_name": "loadBalancerDnsName",
        "security_group_allows_all_outbound": "securityGroupAllowsAllOutbound",
        "vpc": "vpc",
    },
)
class ApplicationLoadBalancerAttributes:
    def __init__(
        self,
        *,
        load_balancer_arn: builtins.str,
        security_group_id: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> None:
        '''(experimental) Properties to reference an existing load balancer.

        :param load_balancer_arn: (experimental) ARN of the load balancer.
        :param security_group_id: (experimental) ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: (experimental) The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: (experimental) The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: (experimental) Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param vpc: (experimental) The VPC this load balancer has been created in, if available. Default: - If the Load Balancer was imported and a VPC was not specified, the VPC is not available.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_arn": load_balancer_arn,
            "security_group_id": security_group_id,
        }
        if load_balancer_canonical_hosted_zone_id is not None:
            self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None:
            self._values["load_balancer_dns_name"] = load_balancer_dns_name
        if security_group_allows_all_outbound is not None:
            self._values["security_group_allows_all_outbound"] = security_group_allows_all_outbound
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) ARN of the load balancer.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''(experimental) ID of the load balancer's security group.

        :stability: experimental
        '''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The canonical hosted zone ID of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_canonical_hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS name of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_allows_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the security group allows all outbound traffic or not.

        Unless set to ``false``, no egress rules will be added to the security group.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("security_group_allows_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC this load balancer has been created in, if available.

        :default:

        - If the Load Balancer was imported and a VPC was not specified,
        the VPC is not available.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_f30d5663], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancerRedirectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "open": "open",
        "source_port": "sourcePort",
        "source_protocol": "sourceProtocol",
        "target_port": "targetPort",
        "target_protocol": "targetProtocol",
    },
)
class ApplicationLoadBalancerRedirectConfig:
    def __init__(
        self,
        *,
        open: typing.Optional[builtins.bool] = None,
        source_port: typing.Optional[jsii.Number] = None,
        source_protocol: typing.Optional["ApplicationProtocol"] = None,
        target_port: typing.Optional[jsii.Number] = None,
        target_protocol: typing.Optional["ApplicationProtocol"] = None,
    ) -> None:
        '''(experimental) Properties for a redirection config.

        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param source_port: (experimental) The port number to listen to. Default: 80
        :param source_protocol: (experimental) The protocol of the listener being created. Default: HTTP
        :param target_port: (experimental) The port number to redirect to. Default: 443
        :param target_protocol: (experimental) The protocol of the redirection target. Default: HTTPS

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if open is not None:
            self._values["open"] = open
        if source_port is not None:
            self._values["source_port"] = source_port
        if source_protocol is not None:
            self._values["source_protocol"] = source_protocol
        if target_port is not None:
            self._values["target_port"] = target_port
        if target_protocol is not None:
            self._values["target_protocol"] = target_protocol

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("open")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port number to listen to.

        :default: 80

        :stability: experimental
        '''
        result = self._values.get("source_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def source_protocol(self) -> typing.Optional["ApplicationProtocol"]:
        '''(experimental) The protocol of the listener being created.

        :default: HTTP

        :stability: experimental
        '''
        result = self._values.get("source_protocol")
        return typing.cast(typing.Optional["ApplicationProtocol"], result)

    @builtins.property
    def target_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port number to redirect to.

        :default: 443

        :stability: experimental
        '''
        result = self._values.get("target_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_protocol(self) -> typing.Optional["ApplicationProtocol"]:
        '''(experimental) The protocol of the redirection target.

        :default: HTTPS

        :stability: experimental
        '''
        result = self._values.get("target_protocol")
        return typing.cast(typing.Optional["ApplicationProtocol"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerRedirectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationProtocol")
class ApplicationProtocol(enum.Enum):
    '''(experimental) Load balancing protocol for application load balancers.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) HTTP.

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) HTTPS.

    :stability: experimental
    '''


@jsii.enum(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationProtocolVersion"
)
class ApplicationProtocolVersion(enum.Enum):
    '''(experimental) Load balancing protocol version for application load balancers.

    :stability: experimental
    '''

    GRPC = "GRPC"
    '''(experimental) GRPC.

    :stability: experimental
    '''
    HTTP1 = "HTTP1"
    '''(experimental) HTTP1.

    :stability: experimental
    '''
    HTTP2 = "HTTP2"
    '''(experimental) HTTP2.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AuthenticateOidcOptions",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_endpoint": "authorizationEndpoint",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "issuer": "issuer",
        "next": "next",
        "token_endpoint": "tokenEndpoint",
        "user_info_endpoint": "userInfoEndpoint",
        "authentication_request_extra_params": "authenticationRequestExtraParams",
        "on_unauthenticated_request": "onUnauthenticatedRequest",
        "scope": "scope",
        "session_cookie_name": "sessionCookieName",
        "session_timeout": "sessionTimeout",
    },
)
class AuthenticateOidcOptions:
    def __init__(
        self,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: _SecretValue_3dd0ddae,
        issuer: builtins.str,
        next: "ListenerAction",
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional["UnauthenticatedAction"] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[_Duration_4839e8c3] = None,
    ) -> None:
        '''(experimental) Options for ``ListenerAction.authenciateOidc()``.

        :param authorization_endpoint: (experimental) The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param client_id: (experimental) The OAuth 2.0 client identifier.
        :param client_secret: (experimental) The OAuth 2.0 client secret.
        :param issuer: (experimental) The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param next: (experimental) What action to execute next.
        :param token_endpoint: (experimental) The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param user_info_endpoint: (experimental) The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param authentication_request_extra_params: (experimental) The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: (experimental) The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: (experimental) The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: (experimental) The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: (experimental) The maximum duration of the authentication session. Default: Duration.days(7)

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "authorization_endpoint": authorization_endpoint,
            "client_id": client_id,
            "client_secret": client_secret,
            "issuer": issuer,
            "next": next,
            "token_endpoint": token_endpoint,
            "user_info_endpoint": user_info_endpoint,
        }
        if authentication_request_extra_params is not None:
            self._values["authentication_request_extra_params"] = authentication_request_extra_params
        if on_unauthenticated_request is not None:
            self._values["on_unauthenticated_request"] = on_unauthenticated_request
        if scope is not None:
            self._values["scope"] = scope
        if session_cookie_name is not None:
            self._values["session_cookie_name"] = session_cookie_name
        if session_timeout is not None:
            self._values["session_timeout"] = session_timeout

    @builtins.property
    def authorization_endpoint(self) -> builtins.str:
        '''(experimental) The authorization endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.

        :stability: experimental
        '''
        result = self._values.get("authorization_endpoint")
        assert result is not None, "Required property 'authorization_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> builtins.str:
        '''(experimental) The OAuth 2.0 client identifier.

        :stability: experimental
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> _SecretValue_3dd0ddae:
        '''(experimental) The OAuth 2.0 client secret.

        :stability: experimental
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(_SecretValue_3dd0ddae, result)

    @builtins.property
    def issuer(self) -> builtins.str:
        '''(experimental) The OIDC issuer identifier of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.

        :stability: experimental
        '''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def next(self) -> "ListenerAction":
        '''(experimental) What action to execute next.

        :stability: experimental
        '''
        result = self._values.get("next")
        assert result is not None, "Required property 'next' is missing"
        return typing.cast("ListenerAction", result)

    @builtins.property
    def token_endpoint(self) -> builtins.str:
        '''(experimental) The token endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.

        :stability: experimental
        '''
        result = self._values.get("token_endpoint")
        assert result is not None, "Required property 'token_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_info_endpoint(self) -> builtins.str:
        '''(experimental) The user info endpoint of the IdP.

        This must be a full URL, including the HTTPS protocol, the domain, and the path.

        :stability: experimental
        '''
        result = self._values.get("user_info_endpoint")
        assert result is not None, "Required property 'user_info_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_request_extra_params(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

        :default: - No extra parameters

        :stability: experimental
        '''
        result = self._values.get("authentication_request_extra_params")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_unauthenticated_request(self) -> typing.Optional["UnauthenticatedAction"]:
        '''(experimental) The behavior if the user is not authenticated.

        :default: UnauthenticatedAction.AUTHENTICATE

        :stability: experimental
        '''
        result = self._values.get("on_unauthenticated_request")
        return typing.cast(typing.Optional["UnauthenticatedAction"], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''(experimental) The set of user claims to be requested from the IdP.

        To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

        :default: "openid"

        :stability: experimental
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_cookie_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the cookie used to maintain session information.

        :default: "AWSELBAuthSessionCookie"

        :stability: experimental
        '''
        result = self._values.get("session_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_timeout(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The maximum duration of the authentication session.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("session_timeout")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthenticateOidcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseApplicationListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "open": "open",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class BaseApplicationListenerProps:
    def __init__(
        self,
        *,
        certificates: typing.Optional[typing.Sequence["IListenerCertificate"]] = None,
        default_action: typing.Optional["ListenerAction"] = None,
        default_target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        '''(experimental) Basic properties for an ApplicationListener.

        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if open is not None:
            self._values["open"] = open
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        '''(experimental) Certificate list of ACM cert ARNs.

        :default: - No certificates.

        :stability: experimental
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List["IListenerCertificate"]], result)

    @builtins.property
    def default_action(self) -> typing.Optional["ListenerAction"]:
        '''(experimental) Default action to take for requests to this listener.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses.

        See the ``ListenerAction`` class for all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional["ListenerAction"], result)

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        '''(experimental) Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_target_groups")
        return typing.cast(typing.Optional[typing.List["IApplicationTargetGroup"]], result)

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("open")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port on which the listener listens for requests.

        :default: - Determined from protocol if known.

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        '''(experimental) The protocol to use.

        :default: - Determined from port if known.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ApplicationProtocol], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        '''(experimental) The security policy that defines which ciphers and protocols are supported.

        :default: - The current predefined security policy.

        :stability: experimental
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional["SslPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseApplicationListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseApplicationListenerRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "action": "action",
        "conditions": "conditions",
        "target_groups": "targetGroups",
    },
)
class BaseApplicationListenerRuleProps:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        action: typing.Optional["ListenerAction"] = None,
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
    ) -> None:
        '''(experimental) Basic properties for defining a rule on a listener.

        :param priority: (experimental) Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: (experimental) Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param target_groups: (experimental) Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "priority": priority,
        }
        if action is not None:
            self._values["action"] = action
        if conditions is not None:
            self._values["conditions"] = conditions
        if target_groups is not None:
            self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def action(self) -> typing.Optional["ListenerAction"]:
        '''(experimental) Action to perform when requests are received.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No action

        :stability: experimental
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["ListenerAction"], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List["ListenerCondition"]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List["ListenerCondition"]], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        '''(experimental) Target groups to forward requests to.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        Implies a ``forward`` action.

        :default: - No target groups.

        :stability: experimental
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List["IApplicationTargetGroup"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseApplicationListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseListener(
    _Resource_45bc6135,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseListener",
):
    '''(experimental) Base class for listeners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        additional_props: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param additional_props: -

        :stability: experimental
        '''
        jsii.create(BaseListener, self, [scope, id, additional_props])

    @jsii.member(jsii_name="validateListener")
    def _validate_listener(self) -> typing.List[builtins.str]:
        '''(experimental) Validate this listener.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateListener", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))


class _BaseListenerProxy(
    BaseListener, jsii.proxy_for(_Resource_45bc6135) # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseListener).__jsii_proxy_class__ = lambda : _BaseListenerProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseListenerLookupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class BaseListenerLookupOptions:
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for listener lookup.

        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: (experimental) Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: (experimental) Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Filter listeners by listener port.

        :default: - does not filter by listener port

        :stability: experimental
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseLoadBalancer(
    _Resource_45bc6135,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseLoadBalancer",
):
    '''(experimental) Base class for both Application and Network Load Balancers.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        base_props: "BaseLoadBalancerProps",
        additional_props: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -

        :stability: experimental
        '''
        jsii.create(BaseLoadBalancer, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(
        self,
        bucket: _IBucket_42e086fd,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Enable access logging for this load balancer.

        A region must be specified on the stack containing the load balancer; you cannot enable logging on
        environment-agnostic stacks. See https://docs.aws.amazon.com/cdk/latest/guide/environments.html

        :param bucket: -
        :param prefix: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "logAccessLogs", [bucket, prefix]))

    @jsii.member(jsii_name="removeAttribute")
    def remove_attribute(self, key: builtins.str) -> None:
        '''(experimental) Remove an attribute from the load balancer.

        :param key: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "removeAttribute", [key]))

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Set a non-standard attribute on the load balancer.

        :param key: -
        :param value: -

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#load-balancer-attributes
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "setAttribute", [key, value]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) The ARN of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:elasticloadbalancing:us-west-2123456789012loadbalancer / app / my - internal - load - balancer / 50dc6c495c0c9188
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The canonical hosted zone ID of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerCanonicalHostedZoneId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        '''(experimental) The DNS name of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerDnsName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerFullName")
    def load_balancer_full_name(self) -> builtins.str:
        '''(experimental) The full name of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 50dc6c495c0c9188
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerFullName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerName")
    def load_balancer_name(self) -> builtins.str:
        '''(experimental) The name of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerSecurityGroups")
    def load_balancer_security_groups(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerSecurityGroups"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_f30d5663:
        '''(experimental) The VPC this load balancer has been created in.

        :stability: experimental
        '''
        return typing.cast(_IVpc_f30d5663, jsii.get(self, "vpc"))


class _BaseLoadBalancerProxy(
    BaseLoadBalancer, jsii.proxy_for(_Resource_45bc6135) # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseLoadBalancer).__jsii_proxy_class__ = lambda : _BaseLoadBalancerProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseLoadBalancerLookupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class BaseLoadBalancerLookupOptions:
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for looking up load balancers.

        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
    },
)
class BaseLoadBalancerProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_f30d5663,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_e57d76df] = None,
    ) -> None:
        '''(experimental) Shared properties of both Application and Network Load Balancers.

        :param vpc: (experimental) The VPC network to place the load balancer in.
        :param deletion_protection: (experimental) Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: (experimental) Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: (experimental) Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: (experimental) Which subnets place the load balancer in. Default: - the Vpc default strategy.

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_e57d76df(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_f30d5663:
        '''(experimental) The VPC network to place the load balancer in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_f30d5663, result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether deletion protection is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the load balancer has an internet-routable address.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the load balancer.

        :default: - Automatically generated name.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_e57d76df]:
        '''(experimental) Which subnets place the load balancer in.

        :default: - the Vpc default strategy.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_e57d76df], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseNetworkListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "port": "port",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class BaseNetworkListenerProps:
    def __init__(
        self,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence["IListenerCertificate"]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        '''(experimental) Basic properties for a Network Listener.

        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The port on which the listener listens for requests.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List["IListenerCertificate"]]:
        '''(experimental) Certificate list of ACM cert ARNs.

        :default: - No certificates.

        :stability: experimental
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List["IListenerCertificate"]], result)

    @builtins.property
    def default_action(self) -> typing.Optional["NetworkListenerAction"]:
        '''(experimental) Default action to take for requests to this listener.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional["NetworkListenerAction"], result)

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        '''(experimental) Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_target_groups")
        return typing.cast(typing.Optional[typing.List["INetworkTargetGroup"]], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TLS if certificates are provided. TCP otherwise.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        '''(experimental) SSL Policy.

        :default: - Current predefined security policy.

        :stability: experimental
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional["SslPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseNetworkListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.BaseTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
    },
)
class BaseTargetGroupProps:
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional["HealthCheck"] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional["TargetType"] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> None:
        '''(experimental) Basic properties of both Application and Network Target Groups.

        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: (experimental) Health check configuration. Default: - None.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: (experimental) The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: (experimental) The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheck"]:
        '''(experimental) Health check configuration.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheck"], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.

        :stability: experimental
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        '''(experimental) The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.

        :stability: experimental
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional["TargetType"], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_f30d5663], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnListener(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancingV2::Listener``.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::Listener
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        default_actions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListener.ActionProperty", _IResolvable_da3f097b]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificates: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListener.CertificateProperty", _IResolvable_da3f097b]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancingV2::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param alpn_policy: ``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.
        '''
        props = CfnListenerProps(
            default_actions=default_actions,
            load_balancer_arn=load_balancer_arn,
            alpn_policy=alpn_policy,
            certificates=certificates,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(CfnListener, self, [scope, id, props])

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ListenerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrListenerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultActions")
    def default_actions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.ActionProperty", _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        '''
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.ActionProperty", _IResolvable_da3f097b]]], jsii.get(self, "defaultActions"))

    @default_actions.setter
    def default_actions(
        self,
        value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.ActionProperty", _IResolvable_da3f097b]]],
    ) -> None:
        jsii.set(self, "defaultActions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArn"))

    @load_balancer_arn.setter
    def load_balancer_arn(self, value: builtins.str) -> None:
        jsii.set(self, "loadBalancerArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alpnPolicy")
    def alpn_policy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-alpnpolicy
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "alpnPolicy"))

    @alpn_policy.setter
    def alpn_policy(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "alpnPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.CertificateProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.CertificateProperty", _IResolvable_da3f097b]]]], jsii.get(self, "certificates"))

    @certificates.setter
    def certificates(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.CertificateProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "certificates", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sslPolicy")
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sslPolicy"))

    @ssl_policy.setter
    def ssl_policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sslPolicy", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            authenticate_cognito_config: typing.Optional[typing.Union["CfnListener.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union["CfnListener.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]] = None,
            fixed_response_config: typing.Optional[typing.Union["CfnListener.FixedResponseConfigProperty", _IResolvable_da3f097b]] = None,
            forward_config: typing.Optional[typing.Union["CfnListener.ForwardConfigProperty", _IResolvable_da3f097b]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union["CfnListener.RedirectConfigProperty", _IResolvable_da3f097b]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: ``CfnListener.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListener.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListener.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListener.ActionProperty.FixedResponseConfig``.
            :param forward_config: ``CfnListener.ActionProperty.ForwardConfig``.
            :param order: ``CfnListener.ActionProperty.Order``.
            :param redirect_config: ``CfnListener.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListener.ActionProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnListener.ActionProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ActionProperty.AuthenticateCognitoConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticatecognitoconfig
            '''
            result = self._values.get("authenticate_cognito_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ActionProperty.AuthenticateOidcConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticateoidcconfig
            '''
            result = self._values.get("authenticate_oidc_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.FixedResponseConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ActionProperty.FixedResponseConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-fixedresponseconfig
            '''
            result = self._values.get("fixed_response_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.FixedResponseConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.ForwardConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ActionProperty.ForwardConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-forwardconfig
            '''
            result = self._values.get("forward_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.ForwardConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''``CfnListener.ActionProperty.Order``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.RedirectConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ActionProperty.RedirectConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-redirectconfig
            '''
            result = self._values.get("redirect_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.RedirectConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.ActionProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            user_pool_arn: builtins.str,
            user_pool_client_id: builtins.str,
            user_pool_domain: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param user_pool_arn: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "user_pool_arn": user_pool_arn,
                "user_pool_client_id": user_pool_client_id,
                "user_pool_domain": user_pool_domain,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> builtins.str:
            '''``CfnListener.AuthenticateCognitoConfigProperty.UserPoolArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            assert result is not None, "Required property 'user_pool_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_pool_client_id(self) -> builtins.str:
            '''``CfnListener.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolclientid
            '''
            result = self._values.get("user_pool_client_id")
            assert result is not None, "Required property 'user_pool_client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_pool_domain(self) -> builtins.str:
            '''``CfnListener.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpooldomain
            '''
            result = self._values.get("user_pool_domain")
            assert result is not None, "Required property 'user_pool_domain' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnListener.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateCognitoConfigProperty.Scope``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateCognitoConfigProperty.SessionCookieName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "token_endpoint": "tokenEndpoint",
            "user_info_endpoint": "userInfoEndpoint",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authorization_endpoint: builtins.str,
            client_id: builtins.str,
            client_secret: builtins.str,
            issuer: builtins.str,
            token_endpoint: builtins.str,
            user_info_endpoint: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param authorization_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListener.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListener.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListener.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "authorization_endpoint": authorization_endpoint,
                "client_id": client_id,
                "client_secret": client_secret,
                "issuer": issuer,
                "token_endpoint": token_endpoint,
                "user_info_endpoint": user_info_endpoint,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def authorization_endpoint(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authorizationendpoint
            '''
            result = self._values.get("authorization_endpoint")
            assert result is not None, "Required property 'authorization_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def issuer(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.Issuer``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-issuer
            '''
            result = self._values.get("issuer")
            assert result is not None, "Required property 'issuer' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def token_endpoint(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.TokenEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-tokenendpoint
            '''
            result = self._values.get("token_endpoint")
            assert result is not None, "Required property 'token_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_info_endpoint(self) -> builtins.str:
            '''``CfnListener.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-userinfoendpoint
            '''
            result = self._values.get("user_info_endpoint")
            assert result is not None, "Required property 'user_info_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnListener.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateOidcConfigProperty.Scope``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateOidcConfigProperty.SessionCookieName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.AuthenticateOidcConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnListener.CertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.CertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html#cfn-elasticloadbalancingv2-listener-certificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "content_type": "contentType",
            "message_body": "messageBody",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param status_code: ``CfnListener.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListener.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListener.FixedResponseConfigProperty.MessageBody``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> builtins.str:
            '''``CfnListener.FixedResponseConfigProperty.StatusCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.FixedResponseConfigProperty.ContentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.FixedResponseConfigProperty.MessageBody``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-messagebody
            '''
            result = self._values.get("message_body")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListener.TargetGroupTupleProperty", _IResolvable_da3f097b]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union["CfnListener.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param target_groups: ``CfnListener.ForwardConfigProperty.TargetGroups``.
            :param target_group_stickiness_config: ``CfnListener.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.TargetGroupTupleProperty", _IResolvable_da3f097b]]]]:
            '''``CfnListener.ForwardConfigProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListener.TargetGroupTupleProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListener.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListener.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroupstickinessconfig
            '''
            result = self._values.get("target_group_stickiness_config")
            return typing.cast(typing.Optional[typing.Union["CfnListener.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param status_code: ``CfnListener.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListener.RedirectConfigProperty.Host``.
            :param path: ``CfnListener.RedirectConfigProperty.Path``.
            :param port: ``CfnListener.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListener.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListener.RedirectConfigProperty.Query``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query

        @builtins.property
        def status_code(self) -> builtins.str:
            '''``CfnListener.RedirectConfigProperty.StatusCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.RedirectConfigProperty.Host``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.RedirectConfigProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.RedirectConfigProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.RedirectConfigProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.RedirectConfigProperty.Query``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param duration_seconds: ``CfnListener.TargetGroupStickinessConfigProperty.DurationSeconds``.
            :param enabled: ``CfnListener.TargetGroupStickinessConfigProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnListener.TargetGroupStickinessConfigProperty.DurationSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-durationseconds
            '''
            result = self._values.get("duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnListener.TargetGroupStickinessConfigProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListener.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param target_group_arn: ``CfnListener.TargetGroupTupleProperty.TargetGroupArn``.
            :param weight: ``CfnListener.TargetGroupTupleProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListener.TargetGroupTupleProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnListener.TargetGroupTupleProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_c2943556)
class CfnListenerCertificate(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerCertificate",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerCertificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        certificates: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListenerCertificate.CertificateProperty", _IResolvable_da3f097b]]],
        listener_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.
        '''
        props = CfnListenerCertificateProps(
            certificates=certificates, listener_arn=listener_arn
        )

        jsii.create(CfnListenerCertificate, self, [scope, id, props])

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificates")
    def certificates(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerCertificate.CertificateProperty", _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        '''
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerCertificate.CertificateProperty", _IResolvable_da3f097b]]], jsii.get(self, "certificates"))

    @certificates.setter
    def certificates(
        self,
        value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerCertificate.CertificateProperty", _IResolvable_da3f097b]]],
    ) -> None:
        jsii.set(self, "certificates", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @listener_arn.setter
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerCertificate.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_arn: ``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerCertificate.CertificateProperty.CertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificates.html#cfn-elasticloadbalancingv2-listener-certificates-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={"certificates": "certificates", "listener_arn": "listenerArn"},
)
class CfnListenerCertificateProps:
    def __init__(
        self,
        *,
        certificates: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnListenerCertificate.CertificateProperty, _IResolvable_da3f097b]]],
        listener_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param certificates: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "certificates": certificates,
            "listener_arn": listener_arn,
        }

    @builtins.property
    def certificates(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerCertificate.CertificateProperty, _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerCertificate.Certificates``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        '''
        result = self._values.get("certificates")
        assert result is not None, "Required property 'certificates' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerCertificate.CertificateProperty, _IResolvable_da3f097b]]], result)

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::ListenerCertificate.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_actions": "defaultActions",
        "load_balancer_arn": "loadBalancerArn",
        "alpn_policy": "alpnPolicy",
        "certificates": "certificates",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        default_actions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnListener.ActionProperty, _IResolvable_da3f097b]]],
        load_balancer_arn: builtins.str,
        alpn_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificates: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnListener.CertificateProperty, _IResolvable_da3f097b]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ElasticLoadBalancingV2::Listener``.

        :param default_actions: ``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.
        :param load_balancer_arn: ``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.
        :param alpn_policy: ``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.
        :param certificates: ``AWS::ElasticLoadBalancingV2::Listener.Certificates``.
        :param port: ``AWS::ElasticLoadBalancingV2::Listener.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::Listener.Protocol``.
        :param ssl_policy: ``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "default_actions": default_actions,
            "load_balancer_arn": load_balancer_arn,
        }
        if alpn_policy is not None:
            self._values["alpn_policy"] = alpn_policy
        if certificates is not None:
            self._values["certificates"] = certificates
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def default_actions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListener.ActionProperty, _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.DefaultActions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        '''
        result = self._values.get("default_actions")
        assert result is not None, "Required property 'default_actions' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListener.ActionProperty, _IResolvable_da3f097b]]], result)

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::Listener.LoadBalancerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        '''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alpn_policy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.AlpnPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-alpnpolicy
        '''
        result = self._values.get("alpn_policy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListener.CertificateProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Certificates``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListener.CertificateProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::Listener.SslPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnListenerRule(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancingV2::ListenerRule``.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        actions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListenerRule.ActionProperty", _IResolvable_da3f097b]]],
        conditions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListenerRule.RuleConditionProperty", _IResolvable_da3f097b]]],
        listener_arn: builtins.str,
        priority: jsii.Number,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.
        '''
        props = CfnListenerRuleProps(
            actions=actions,
            conditions=conditions,
            listener_arn=listener_arn,
            priority=priority,
        )

        jsii.create(CfnListenerRule, self, [scope, id, props])

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrIsDefault")
    def attr_is_default(self) -> _IResolvable_da3f097b:
        '''
        :cloudformationAttribute: IsDefault
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrIsDefault"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRuleArn")
    def attr_rule_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: RuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.ActionProperty", _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        '''
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.ActionProperty", _IResolvable_da3f097b]]], jsii.get(self, "actions"))

    @actions.setter
    def actions(
        self,
        value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.ActionProperty", _IResolvable_da3f097b]]],
    ) -> None:
        jsii.set(self, "actions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="conditions")
    def conditions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.RuleConditionProperty", _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        '''
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.RuleConditionProperty", _IResolvable_da3f097b]]], jsii.get(self, "conditions"))

    @conditions.setter
    def conditions(
        self,
        value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.RuleConditionProperty", _IResolvable_da3f097b]]],
    ) -> None:
        jsii.set(self, "conditions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @listener_arn.setter
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        jsii.set(self, "priority", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            authenticate_cognito_config: typing.Optional[typing.Union["CfnListenerRule.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union["CfnListenerRule.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]] = None,
            fixed_response_config: typing.Optional[typing.Union["CfnListenerRule.FixedResponseConfigProperty", _IResolvable_da3f097b]] = None,
            forward_config: typing.Optional[typing.Union["CfnListenerRule.ForwardConfigProperty", _IResolvable_da3f097b]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union["CfnListenerRule.RedirectConfigProperty", _IResolvable_da3f097b]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param type: ``CfnListenerRule.ActionProperty.Type``.
            :param authenticate_cognito_config: ``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.
            :param authenticate_oidc_config: ``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.
            :param fixed_response_config: ``CfnListenerRule.ActionProperty.FixedResponseConfig``.
            :param forward_config: ``CfnListenerRule.ActionProperty.ForwardConfig``.
            :param order: ``CfnListenerRule.ActionProperty.Order``.
            :param redirect_config: ``CfnListenerRule.ActionProperty.RedirectConfig``.
            :param target_group_arn: ``CfnListenerRule.ActionProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
            }
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnListenerRule.ActionProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ActionProperty.AuthenticateCognitoConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticatecognitoconfig
            '''
            result = self._values.get("authenticate_cognito_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.AuthenticateCognitoConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ActionProperty.AuthenticateOidcConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticateoidcconfig
            '''
            result = self._values.get("authenticate_oidc_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.AuthenticateOidcConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.FixedResponseConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ActionProperty.FixedResponseConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-fixedresponseconfig
            '''
            result = self._values.get("fixed_response_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.FixedResponseConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.ForwardConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ActionProperty.ForwardConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-forwardconfig
            '''
            result = self._values.get("forward_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.ForwardConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''``CfnListenerRule.ActionProperty.Order``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.RedirectConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ActionProperty.RedirectConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-redirectconfig
            '''
            result = self._values.get("redirect_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.RedirectConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.ActionProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            user_pool_arn: builtins.str,
            user_pool_client_id: builtins.str,
            user_pool_domain: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param user_pool_arn: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.
            :param user_pool_client_id: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.
            :param user_pool_domain: ``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "user_pool_arn": user_pool_arn,
                "user_pool_client_id": user_pool_client_id,
                "user_pool_domain": user_pool_domain,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout

        @builtins.property
        def user_pool_arn(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            assert result is not None, "Required property 'user_pool_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_pool_client_id(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolclientid
            '''
            result = self._values.get("user_pool_client_id")
            assert result is not None, "Required property 'user_pool_client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_pool_domain(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.UserPoolDomain``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpooldomain
            '''
            result = self._values.get("user_pool_domain")
            assert result is not None, "Required property 'user_pool_domain' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.AuthenticationRequestExtraParams``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.OnUnauthenticatedRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.Scope``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionCookieName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''``CfnListenerRule.AuthenticateCognitoConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "token_endpoint": "tokenEndpoint",
            "user_info_endpoint": "userInfoEndpoint",
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
            "use_existing_client_secret": "useExistingClientSecret",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authorization_endpoint: builtins.str,
            client_id: builtins.str,
            client_secret: builtins.str,
            issuer: builtins.str,
            token_endpoint: builtins.str,
            user_info_endpoint: builtins.str,
            authentication_request_extra_params: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
            use_existing_client_secret: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param authorization_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.
            :param client_id: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.
            :param client_secret: ``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.
            :param issuer: ``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.
            :param token_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.
            :param user_info_endpoint: ``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.
            :param authentication_request_extra_params: ``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.
            :param on_unauthenticated_request: ``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.
            :param scope: ``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.
            :param session_cookie_name: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.
            :param session_timeout: ``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.
            :param use_existing_client_secret: ``CfnListenerRule.AuthenticateOidcConfigProperty.UseExistingClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "authorization_endpoint": authorization_endpoint,
                "client_id": client_id,
                "client_secret": client_secret,
                "issuer": issuer,
                "token_endpoint": token_endpoint,
                "user_info_endpoint": user_info_endpoint,
            }
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if use_existing_client_secret is not None:
                self._values["use_existing_client_secret"] = use_existing_client_secret

        @builtins.property
        def authorization_endpoint(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.AuthorizationEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authorizationendpoint
            '''
            result = self._values.get("authorization_endpoint")
            assert result is not None, "Required property 'authorization_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def issuer(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.Issuer``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-issuer
            '''
            result = self._values.get("issuer")
            assert result is not None, "Required property 'issuer' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def token_endpoint(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.TokenEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-tokenendpoint
            '''
            result = self._values.get("token_endpoint")
            assert result is not None, "Required property 'token_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_info_endpoint(self) -> builtins.str:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.UserInfoEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-userinfoendpoint
            '''
            result = self._values.get("user_info_endpoint")
            assert result is not None, "Required property 'user_info_endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.AuthenticationRequestExtraParams``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.OnUnauthenticatedRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.Scope``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.SessionCookieName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.SessionTimeout``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def use_existing_client_secret(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnListenerRule.AuthenticateOidcConfigProperty.UseExistingClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-useexistingclientsecret
            '''
            result = self._values.get("use_existing_client_secret")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "content_type": "contentType",
            "message_body": "messageBody",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param status_code: ``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.
            :param content_type: ``CfnListenerRule.FixedResponseConfigProperty.ContentType``.
            :param message_body: ``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body

        @builtins.property
        def status_code(self) -> builtins.str:
            '''``CfnListenerRule.FixedResponseConfigProperty.StatusCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.FixedResponseConfigProperty.ContentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.FixedResponseConfigProperty.MessageBody``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-messagebody
            '''
            result = self._values.get("message_body")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListenerRule.TargetGroupTupleProperty", _IResolvable_da3f097b]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union["CfnListenerRule.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param target_groups: ``CfnListenerRule.ForwardConfigProperty.TargetGroups``.
            :param target_group_stickiness_config: ``CfnListenerRule.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.TargetGroupTupleProperty", _IResolvable_da3f097b]]]]:
            '''``CfnListenerRule.ForwardConfigProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.TargetGroupTupleProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.ForwardConfigProperty.TargetGroupStickinessConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroupstickinessconfig
            '''
            result = self._values.get("target_group_stickiness_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.TargetGroupStickinessConfigProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.HostHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class HostHeaderConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param values: ``CfnListenerRule.HostHeaderConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.HostHeaderConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-hostheaderconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.HttpHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"http_header_name": "httpHeaderName", "values": "values"},
    )
    class HttpHeaderConfigProperty:
        def __init__(
            self,
            *,
            http_header_name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param http_header_name: ``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.
            :param values: ``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if http_header_name is not None:
                self._values["http_header_name"] = http_header_name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def http_header_name(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.HttpHeaderConfigProperty.HttpHeaderName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-httpheadername
            '''
            result = self._values.get("http_header_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.HttpHeaderConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.HttpRequestMethodConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class HttpRequestMethodConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param values: ``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.HttpRequestMethodConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html#cfn-elasticloadbalancingv2-listenerrule-httprequestmethodconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRequestMethodConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.PathPatternConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class PathPatternConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param values: ``CfnListenerRule.PathPatternConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.PathPatternConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html#cfn-elasticloadbalancingv2-listenerrule-pathpatternconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathPatternConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.QueryStringConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class QueryStringConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnListenerRule.QueryStringKeyValueProperty", _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''
            :param values: ``CfnListenerRule.QueryStringConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.QueryStringKeyValueProperty", _IResolvable_da3f097b]]]]:
            '''``CfnListenerRule.QueryStringConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html#cfn-elasticloadbalancingv2-listenerrule-querystringconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnListenerRule.QueryStringKeyValueProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.QueryStringKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class QueryStringKeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnListenerRule.QueryStringKeyValueProperty.Key``.
            :param value: ``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.QueryStringKeyValueProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.QueryStringKeyValueProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status_code": "statusCode",
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            status_code: builtins.str,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param status_code: ``CfnListenerRule.RedirectConfigProperty.StatusCode``.
            :param host: ``CfnListenerRule.RedirectConfigProperty.Host``.
            :param path: ``CfnListenerRule.RedirectConfigProperty.Path``.
            :param port: ``CfnListenerRule.RedirectConfigProperty.Port``.
            :param protocol: ``CfnListenerRule.RedirectConfigProperty.Protocol``.
            :param query: ``CfnListenerRule.RedirectConfigProperty.Query``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status_code": status_code,
            }
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query

        @builtins.property
        def status_code(self) -> builtins.str:
            '''``CfnListenerRule.RedirectConfigProperty.StatusCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RedirectConfigProperty.Host``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RedirectConfigProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RedirectConfigProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RedirectConfigProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RedirectConfigProperty.Query``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field": "field",
            "host_header_config": "hostHeaderConfig",
            "http_header_config": "httpHeaderConfig",
            "http_request_method_config": "httpRequestMethodConfig",
            "path_pattern_config": "pathPatternConfig",
            "query_string_config": "queryStringConfig",
            "source_ip_config": "sourceIpConfig",
            "values": "values",
        },
    )
    class RuleConditionProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            host_header_config: typing.Optional[typing.Union["CfnListenerRule.HostHeaderConfigProperty", _IResolvable_da3f097b]] = None,
            http_header_config: typing.Optional[typing.Union["CfnListenerRule.HttpHeaderConfigProperty", _IResolvable_da3f097b]] = None,
            http_request_method_config: typing.Optional[typing.Union["CfnListenerRule.HttpRequestMethodConfigProperty", _IResolvable_da3f097b]] = None,
            path_pattern_config: typing.Optional[typing.Union["CfnListenerRule.PathPatternConfigProperty", _IResolvable_da3f097b]] = None,
            query_string_config: typing.Optional[typing.Union["CfnListenerRule.QueryStringConfigProperty", _IResolvable_da3f097b]] = None,
            source_ip_config: typing.Optional[typing.Union["CfnListenerRule.SourceIpConfigProperty", _IResolvable_da3f097b]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param field: ``CfnListenerRule.RuleConditionProperty.Field``.
            :param host_header_config: ``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.
            :param http_header_config: ``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.
            :param http_request_method_config: ``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.
            :param path_pattern_config: ``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.
            :param query_string_config: ``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.
            :param source_ip_config: ``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.
            :param values: ``CfnListenerRule.RuleConditionProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if host_header_config is not None:
                self._values["host_header_config"] = host_header_config
            if http_header_config is not None:
                self._values["http_header_config"] = http_header_config
            if http_request_method_config is not None:
                self._values["http_request_method_config"] = http_request_method_config
            if path_pattern_config is not None:
                self._values["path_pattern_config"] = path_pattern_config
            if query_string_config is not None:
                self._values["query_string_config"] = query_string_config
            if source_ip_config is not None:
                self._values["source_ip_config"] = source_ip_config
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.RuleConditionProperty.Field``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_header_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.HostHeaderConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.HostHeaderConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-hostheaderconfig
            '''
            result = self._values.get("host_header_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.HostHeaderConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def http_header_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.HttpHeaderConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.HttpHeaderConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httpheaderconfig
            '''
            result = self._values.get("http_header_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.HttpHeaderConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def http_request_method_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.HttpRequestMethodConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.HttpRequestMethodConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httprequestmethodconfig
            '''
            result = self._values.get("http_request_method_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.HttpRequestMethodConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def path_pattern_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.PathPatternConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.PathPatternConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-pathpatternconfig
            '''
            result = self._values.get("path_pattern_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.PathPatternConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def query_string_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.QueryStringConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.QueryStringConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-querystringconfig
            '''
            result = self._values.get("query_string_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.QueryStringConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def source_ip_config(
            self,
        ) -> typing.Optional[typing.Union["CfnListenerRule.SourceIpConfigProperty", _IResolvable_da3f097b]]:
            '''``CfnListenerRule.RuleConditionProperty.SourceIpConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-sourceipconfig
            '''
            result = self._values.get("source_ip_config")
            return typing.cast(typing.Optional[typing.Union["CfnListenerRule.SourceIpConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.RuleConditionProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.SourceIpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class SourceIpConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param values: ``CfnListenerRule.SourceIpConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnListenerRule.SourceIpConfigProperty.Values``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html#cfn-elasticloadbalancingv2-listenerrule-sourceipconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceIpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param duration_seconds: ``CfnListenerRule.TargetGroupStickinessConfigProperty.DurationSeconds``.
            :param enabled: ``CfnListenerRule.TargetGroupStickinessConfigProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnListenerRule.TargetGroupStickinessConfigProperty.DurationSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-durationseconds
            '''
            result = self._values.get("duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnListenerRule.TargetGroupStickinessConfigProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRule.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param target_group_arn: ``CfnListenerRule.TargetGroupTupleProperty.TargetGroupArn``.
            :param weight: ``CfnListenerRule.TargetGroupTupleProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnListenerRule.TargetGroupTupleProperty.TargetGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnListenerRule.TargetGroupTupleProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnListenerRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "conditions": "conditions",
        "listener_arn": "listenerArn",
        "priority": "priority",
    },
)
class CfnListenerRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnListenerRule.ActionProperty, _IResolvable_da3f097b]]],
        conditions: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnListenerRule.RuleConditionProperty, _IResolvable_da3f097b]]],
        listener_arn: builtins.str,
        priority: jsii.Number,
    ) -> None:
        '''Properties for defining a ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param actions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.
        :param conditions: ``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.
        :param listener_arn: ``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.
        :param priority: ``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "actions": actions,
            "conditions": conditions,
            "listener_arn": listener_arn,
            "priority": priority,
        }

    @builtins.property
    def actions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerRule.ActionProperty, _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Actions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerRule.ActionProperty, _IResolvable_da3f097b]]], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerRule.RuleConditionProperty, _IResolvable_da3f097b]]]:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Conditions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnListenerRule.RuleConditionProperty, _IResolvable_da3f097b]]], result)

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''``AWS::ElasticLoadBalancingV2::ListenerRule.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnLoadBalancer(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnLoadBalancer",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::LoadBalancer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_attributes: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnLoadBalancer.LoadBalancerAttributeProperty", _IResolvable_da3f097b]]]] = None,
        name: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnLoadBalancer.SubnetMappingProperty", _IResolvable_da3f097b]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.
        '''
        props = CfnLoadBalancerProps(
            ip_address_type=ip_address_type,
            load_balancer_attributes=load_balancer_attributes,
            name=name,
            scheme=scheme,
            security_groups=security_groups,
            subnet_mappings=subnet_mappings,
            subnets=subnets,
            tags=tags,
            type=type,
        )

        jsii.create(CfnLoadBalancer, self, [scope, id, props])

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrCanonicalHostedZoneId")
    def attr_canonical_hosted_zone_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: CanonicalHostedZoneID
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCanonicalHostedZoneId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DNSName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrLoadBalancerFullName")
    def attr_load_balancer_full_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: LoadBalancerFullName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLoadBalancerFullName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrLoadBalancerName")
    def attr_load_balancer_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: LoadBalancerName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLoadBalancerName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSecurityGroups")
    def attr_security_groups(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: SecurityGroups
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrSecurityGroups"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ipAddressType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerAttributes")
    def load_balancer_attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.LoadBalancerAttributeProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.LoadBalancerAttributeProperty", _IResolvable_da3f097b]]]], jsii.get(self, "loadBalancerAttributes"))

    @load_balancer_attributes.setter
    def load_balancer_attributes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.LoadBalancerAttributeProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "loadBalancerAttributes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scheme", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroups", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.SubnetMappingProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.SubnetMappingProperty", _IResolvable_da3f097b]]]], jsii.get(self, "subnetMappings"))

    @subnet_mappings.setter
    def subnet_mappings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnLoadBalancer.SubnetMappingProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "subnetMappings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "subnets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnLoadBalancer.LoadBalancerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LoadBalancerAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.
            :param value: ``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnLoadBalancer.LoadBalancerAttributeProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnLoadBalancer.LoadBalancerAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattributes.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnLoadBalancer.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnet_id": "subnetId",
            "allocation_id": "allocationId",
            "i_pv6_address": "iPv6Address",
            "private_i_pv4_address": "privateIPv4Address",
        },
    )
    class SubnetMappingProperty:
        def __init__(
            self,
            *,
            subnet_id: builtins.str,
            allocation_id: typing.Optional[builtins.str] = None,
            i_pv6_address: typing.Optional[builtins.str] = None,
            private_i_pv4_address: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param subnet_id: ``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.
            :param allocation_id: ``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.
            :param i_pv6_address: ``CfnLoadBalancer.SubnetMappingProperty.IPv6Address``.
            :param private_i_pv4_address: ``CfnLoadBalancer.SubnetMappingProperty.PrivateIPv4Address``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "subnet_id": subnet_id,
            }
            if allocation_id is not None:
                self._values["allocation_id"] = allocation_id
            if i_pv6_address is not None:
                self._values["i_pv6_address"] = i_pv6_address
            if private_i_pv4_address is not None:
                self._values["private_i_pv4_address"] = private_i_pv4_address

        @builtins.property
        def subnet_id(self) -> builtins.str:
            '''``CfnLoadBalancer.SubnetMappingProperty.SubnetId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-subnetid
            '''
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allocation_id(self) -> typing.Optional[builtins.str]:
            '''``CfnLoadBalancer.SubnetMappingProperty.AllocationId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-allocationid
            '''
            result = self._values.get("allocation_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def i_pv6_address(self) -> typing.Optional[builtins.str]:
            '''``CfnLoadBalancer.SubnetMappingProperty.IPv6Address``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-ipv6address
            '''
            result = self._values.get("i_pv6_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_i_pv4_address(self) -> typing.Optional[builtins.str]:
            '''``CfnLoadBalancer.SubnetMappingProperty.PrivateIPv4Address``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-privateipv4address
            '''
            result = self._values.get("private_i_pv4_address")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address_type": "ipAddressType",
        "load_balancer_attributes": "loadBalancerAttributes",
        "name": "name",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnet_mappings": "subnetMappings",
        "subnets": "subnets",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLoadBalancerProps:
    def __init__(
        self,
        *,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_attributes: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnLoadBalancer.LoadBalancerAttributeProperty, _IResolvable_da3f097b]]]] = None,
        name: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnLoadBalancer.SubnetMappingProperty, _IResolvable_da3f097b]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param ip_address_type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.
        :param load_balancer_attributes: ``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.
        :param name: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.
        :param scheme: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.
        :param security_groups: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.
        :param subnet_mappings: ``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.
        :param subnets: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.
        :param tags: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.
        :param type: ``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if load_balancer_attributes is not None:
            self._values["load_balancer_attributes"] = load_balancer_attributes
        if name is not None:
            self._values["name"] = name
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnLoadBalancer.LoadBalancerAttributeProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.LoadBalancerAttributes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        '''
        result = self._values.get("load_balancer_attributes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnLoadBalancer.LoadBalancerAttributeProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Scheme``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.SecurityGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnLoadBalancer.SubnetMappingProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.SubnetMappings``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnLoadBalancer.SubnetMappingProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Subnets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::LoadBalancer.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnTargetGroup(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnTargetGroup",
):
    '''A CloudFormation ``AWS::ElasticLoadBalancingV2::TargetGroup``.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::TargetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        matcher: typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        target_group_attributes: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnTargetGroup.TargetGroupAttributeProperty", _IResolvable_da3f097b]]]] = None,
        targets: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union["CfnTargetGroup.TargetDescriptionProperty", _IResolvable_da3f097b]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param protocol_version: ``AWS::ElasticLoadBalancingV2::TargetGroup.ProtocolVersion``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.
        '''
        props = CfnTargetGroupProps(
            health_check_enabled=health_check_enabled,
            health_check_interval_seconds=health_check_interval_seconds,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            health_check_timeout_seconds=health_check_timeout_seconds,
            healthy_threshold_count=healthy_threshold_count,
            matcher=matcher,
            name=name,
            port=port,
            protocol=protocol,
            protocol_version=protocol_version,
            tags=tags,
            target_group_attributes=target_group_attributes,
            targets=targets,
            target_type=target_type,
            unhealthy_threshold_count=unhealthy_threshold_count,
            vpc_id=vpc_id,
        )

        jsii.create(CfnTargetGroup, self, [scope, id, props])

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

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrLoadBalancerArns")
    def attr_load_balancer_arns(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: LoadBalancerArns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrLoadBalancerArns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrTargetGroupFullName")
    def attr_target_group_full_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: TargetGroupFullName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTargetGroupFullName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrTargetGroupName")
    def attr_target_group_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: TargetGroupName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTargetGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "healthCheckEnabled"))

    @health_check_enabled.setter
    def health_check_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "healthCheckEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckIntervalSeconds"))

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPath", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPort"))

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPort", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckProtocol"))

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckTimeoutSeconds")
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckTimeoutSeconds"))

    @health_check_timeout_seconds.setter
    def health_check_timeout_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckTimeoutSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthyThresholdCount")
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdCount"))

    @healthy_threshold_count.setter
    def healthy_threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthyThresholdCount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="matcher")
    def matcher(
        self,
    ) -> typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_da3f097b]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_da3f097b]], jsii.get(self, "matcher"))

    @matcher.setter
    def matcher(
        self,
        value: typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_da3f097b]],
    ) -> None:
        jsii.set(self, "matcher", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocolVersion")
    def protocol_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.ProtocolVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocolversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolVersion"))

    @protocol_version.setter
    def protocol_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "protocolVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupAttributes")
    def target_group_attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetGroupAttributeProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetGroupAttributeProperty", _IResolvable_da3f097b]]]], jsii.get(self, "targetGroupAttributes"))

    @target_group_attributes.setter
    def target_group_attributes(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetGroupAttributeProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "targetGroupAttributes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetDescriptionProperty", _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetDescriptionProperty", _IResolvable_da3f097b]]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTargetGroup.TargetDescriptionProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetType"))

    @target_type.setter
    def target_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "targetType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="unhealthyThresholdCount")
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdCount"))

    @unhealthy_threshold_count.setter
    def unhealthy_threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "unhealthyThresholdCount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc_code": "grpcCode", "http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(
            self,
            *,
            grpc_code: typing.Optional[builtins.str] = None,
            http_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param grpc_code: ``CfnTargetGroup.MatcherProperty.GrpcCode``.
            :param http_code: ``CfnTargetGroup.MatcherProperty.HttpCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if grpc_code is not None:
                self._values["grpc_code"] = grpc_code
            if http_code is not None:
                self._values["http_code"] = http_code

        @builtins.property
        def grpc_code(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.MatcherProperty.GrpcCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-grpccode
            '''
            result = self._values.get("grpc_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.MatcherProperty.HttpCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-httpcode
            '''
            result = self._values.get("http_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatcherProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnTargetGroup.TargetDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "availability_zone": "availabilityZone",
            "port": "port",
        },
    )
    class TargetDescriptionProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            availability_zone: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param id: ``CfnTargetGroup.TargetDescriptionProperty.Id``.
            :param availability_zone: ``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.
            :param port: ``CfnTargetGroup.TargetDescriptionProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnTargetGroup.TargetDescriptionProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.TargetDescriptionProperty.AvailabilityZone``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.TargetDescriptionProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnTargetGroup.TargetGroupAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TargetGroupAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnTargetGroup.TargetGroupAttributeProperty.Key``.
            :param value: ``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.TargetGroupAttributeProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.TargetGroupAttributeProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.CfnTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_enabled": "healthCheckEnabled",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
        "healthy_threshold_count": "healthyThresholdCount",
        "matcher": "matcher",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "tags": "tags",
        "target_group_attributes": "targetGroupAttributes",
        "targets": "targets",
        "target_type": "targetType",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
        "vpc_id": "vpcId",
    },
)
class CfnTargetGroupProps:
    def __init__(
        self,
        *,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        matcher: typing.Optional[typing.Union[CfnTargetGroup.MatcherProperty, _IResolvable_da3f097b]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_f6864754]] = None,
        target_group_attributes: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnTargetGroup.TargetGroupAttributeProperty, _IResolvable_da3f097b]]]] = None,
        targets: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[CfnTargetGroup.TargetDescriptionProperty, _IResolvable_da3f097b]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param health_check_enabled: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.
        :param health_check_interval_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.
        :param health_check_timeout_seconds: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.
        :param healthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.
        :param matcher: ``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.
        :param name: ``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.
        :param port: ``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.
        :param protocol: ``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.
        :param protocol_version: ``AWS::ElasticLoadBalancingV2::TargetGroup.ProtocolVersion``.
        :param tags: ``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.
        :param target_group_attributes: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.
        :param targets: ``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.
        :param target_type: ``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.
        :param unhealthy_threshold_count: ``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.
        :param vpc_id: ``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_timeout_seconds is not None:
            self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if matcher is not None:
            self._values["matcher"] = matcher
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if tags is not None:
            self._values["tags"] = tags
        if target_group_attributes is not None:
            self._values["target_group_attributes"] = target_group_attributes
        if targets is not None:
            self._values["targets"] = targets
        if target_type is not None:
            self._values["target_type"] = target_type
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        '''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthCheckTimeoutSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        '''
        result = self._values.get("health_check_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.HealthyThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        '''
        result = self._values.get("healthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def matcher(
        self,
    ) -> typing.Optional[typing.Union[CfnTargetGroup.MatcherProperty, _IResolvable_da3f097b]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Matcher``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        '''
        result = self._values.get("matcher")
        return typing.cast(typing.Optional[typing.Union[CfnTargetGroup.MatcherProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.ProtocolVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocolversion
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    @builtins.property
    def target_group_attributes(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTargetGroup.TargetGroupAttributeProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.TargetGroupAttributes``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        '''
        result = self._values.get("target_group_attributes")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTargetGroup.TargetGroupAttributeProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTargetGroup.TargetDescriptionProperty, _IResolvable_da3f097b]]]]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTargetGroup.TargetDescriptionProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.TargetType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.UnhealthyThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        '''
        result = self._values.get("unhealthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::ElasticLoadBalancingV2::TargetGroup.VpcId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.FixedResponseOptions",
    jsii_struct_bases=[],
    name_mapping={"content_type": "contentType", "message_body": "messageBody"},
)
class FixedResponseOptions:
    def __init__(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``ListenerAction.fixedResponse()``.

        :param content_type: (experimental) Content Type of the response. Valid Values: text/plain | text/css | text/html | application/javascript | application/json Default: - Automatically determined
        :param message_body: (experimental) The response body. Default: - No body

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if content_type is not None:
            self._values["content_type"] = content_type
        if message_body is not None:
            self._values["message_body"] = message_body

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Content Type of the response.

        Valid Values: text/plain | text/css | text/html | application/javascript | application/json

        :default: - Automatically determined

        :stability: experimental
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_body(self) -> typing.Optional[builtins.str]:
        '''(experimental) The response body.

        :default: - No body

        :stability: experimental
        '''
        result = self._values.get("message_body")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FixedResponseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ForwardOptions",
    jsii_struct_bases=[],
    name_mapping={"stickiness_duration": "stickinessDuration"},
)
class ForwardOptions:
    def __init__(
        self,
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> None:
        '''(experimental) Options for ``ListenerAction.forward()``.

        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if stickiness_duration is not None:
            self._values["stickiness_duration"] = stickiness_duration

    @builtins.property
    def stickiness_duration(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) For how long clients should be directed to the same target group.

        Range between 1 second and 7 days.

        :default: - No stickiness

        :stability: experimental
        '''
        result = self._values.get("stickiness_duration")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForwardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.HealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "healthy_grpc_codes": "healthyGrpcCodes",
        "healthy_http_codes": "healthyHttpCodes",
        "healthy_threshold_count": "healthyThresholdCount",
        "interval": "interval",
        "path": "path",
        "port": "port",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
    },
)
class HealthCheck:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        healthy_grpc_codes: typing.Optional[builtins.str] = None,
        healthy_http_codes: typing.Optional[builtins.str] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_Duration_4839e8c3] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional["Protocol"] = None,
        timeout: typing.Optional[_Duration_4839e8c3] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for configuring a health check.

        :param enabled: (experimental) Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance or ip, health checks are always enabled and cannot be disabled. Default: - Determined automatically.
        :param healthy_grpc_codes: (experimental) GRPC code to use when checking for a successful response from a target. You can specify values between 0 and 99. You can specify multiple values (for example, "0,1") or a range of values (for example, "0-5"). Default: - 12
        :param healthy_http_codes: (experimental) HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: (experimental) The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: (experimental) The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: (experimental) The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: (experimental) The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: (experimental) The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: (experimental) The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: (experimental) The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if healthy_grpc_codes is not None:
            self._values["healthy_grpc_codes"] = healthy_grpc_codes
        if healthy_http_codes is not None:
            self._values["healthy_http_codes"] = healthy_http_codes
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if interval is not None:
            self._values["interval"] = interval
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if timeout is not None:
            self._values["timeout"] = timeout
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether health checks are enabled.

        If the target type is lambda,
        health checks are disabled by default but can be enabled. If the target type
        is instance or ip, health checks are always enabled and cannot be disabled.

        :default: - Determined automatically.

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def healthy_grpc_codes(self) -> typing.Optional[builtins.str]:
        '''(experimental) GRPC code to use when checking for a successful response from a target.

        You can specify values between 0 and 99. You can specify multiple values
        (for example, "0,1") or a range of values (for example, "0-5").

        :default: - 12

        :stability: experimental
        '''
        result = self._values.get("healthy_grpc_codes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def healthy_http_codes(self) -> typing.Optional[builtins.str]:
        '''(experimental) HTTP code to use when checking for a successful response from a target.

        For Application Load Balancers, you can specify values between 200 and
        499, and the default value is 200. You can specify multiple values (for
        example, "200,202") or a range of values (for example, "200-299").

        :stability: experimental
        '''
        result = self._values.get("healthy_http_codes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive health checks successes required before considering an unhealthy target healthy.

        For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3.

        :default: 5 for ALBs, 3 for NLBs

        :stability: experimental
        '''
        result = self._values.get("healthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The approximate number of seconds between health checks for an individual target.

        :default: Duration.seconds(30)

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ping path destination where Elastic Load Balancing sends health check requests.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The port that the load balancer uses when performing health checks on the targets.

        :default: 'traffic-port'

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) The protocol the load balancer uses when performing health checks on targets.

        The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP.
        The TLS, UDP, and TCP_UDP protocols are not supported for health checks.

        :default: HTTP for ALBs, TCP for NLBs

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time, in seconds, during which no response from a target means a failed health check.

        For Application Load Balancers, the range is 2-60 seconds and the
        default is 5 seconds. For Network Load Balancers, this is 10 seconds for
        TCP and HTTPS health checks and 6 seconds for HTTP health checks.

        :default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of consecutive health check failures required before considering a target unhealthy.

        For Application Load Balancers, the default is 2. For Network Load
        Balancers, this value must be the same as the healthy threshold count.

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("unhealthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.HttpCodeElb")
class HttpCodeElb(enum.Enum):
    '''(experimental) Count of HTTP status originating from the load balancer.

    This count does not include any response codes generated by the targets.

    :stability: experimental
    '''

    ELB_3XX_COUNT = "ELB_3XX_COUNT"
    '''(experimental) The number of HTTP 3XX redirection codes that originate from the load balancer.

    :stability: experimental
    '''
    ELB_4XX_COUNT = "ELB_4XX_COUNT"
    '''(experimental) The number of HTTP 4XX client error codes that originate from the load balancer.

    Client errors are generated when requests are malformed or incomplete.
    These requests have not been received by the target. This count does not
    include any response codes generated by the targets.

    :stability: experimental
    '''
    ELB_5XX_COUNT = "ELB_5XX_COUNT"
    '''(experimental) The number of HTTP 5XX server error codes that originate from the load balancer.

    :stability: experimental
    '''


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.HttpCodeTarget")
class HttpCodeTarget(enum.Enum):
    '''(experimental) Count of HTTP status originating from the targets.

    :stability: experimental
    '''

    TARGET_2XX_COUNT = "TARGET_2XX_COUNT"
    '''(experimental) The number of 2xx response codes from targets.

    :stability: experimental
    '''
    TARGET_3XX_COUNT = "TARGET_3XX_COUNT"
    '''(experimental) The number of 3xx response codes from targets.

    :stability: experimental
    '''
    TARGET_4XX_COUNT = "TARGET_4XX_COUNT"
    '''(experimental) The number of 4xx response codes from targets.

    :stability: experimental
    '''
    TARGET_5XX_COUNT = "TARGET_5XX_COUNT"
    '''(experimental) The number of 5xx response codes from targets.

    :stability: experimental
    '''


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationListener"
)
class IApplicationListener(
    _IResource_c80c4260,
    _IConnectable_10015a05,
    typing_extensions.Protocol,
):
    '''(experimental) Properties to reference an existing listener.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addCertificates")
    def add_certificates(
        self,
        id: builtins.str,
        certificates: typing.Sequence["IListenerCertificate"],
    ) -> None:
        '''(experimental) Add one or more certificates to this listener.

        :param id: -
        :param certificates: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.Sequence["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: (experimental) Target groups to forward requests to.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence["IApplicationLoadBalancerTarget"]] = None,
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        '''(experimental) Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: (experimental) The protocol to use. Default: Determined from port if known
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: _Port_85922693,
    ) -> None:
        '''(experimental) Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        ...


class _IApplicationListenerProxy(
    jsii.proxy_for(_IResource_c80c4260), # type: ignore[misc]
    jsii.proxy_for(_IConnectable_10015a05), # type: ignore[misc]
):
    '''(experimental) Properties to reference an existing listener.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationListener"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @jsii.member(jsii_name="addCertificates")
    def add_certificates(
        self,
        id: builtins.str,
        certificates: typing.Sequence["IListenerCertificate"],
    ) -> None:
        '''(experimental) Add one or more certificates to this listener.

        :param id: -
        :param certificates: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addCertificates", [id, certificates]))

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.Sequence["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Load balance incoming requests to the given target groups.

        It's possible to add conditions to the TargetGroups added in this way.
        At least one TargetGroup must be added without conditions.

        :param id: -
        :param target_groups: (experimental) Target groups to forward requests to.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :stability: experimental
        '''
        props = AddApplicationTargetGroupsProps(
            target_groups=target_groups, conditions=conditions, priority=priority
        )

        return typing.cast(None, jsii.invoke(self, "addTargetGroups", [id, props]))

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence["IApplicationLoadBalancerTarget"]] = None,
        conditions: typing.Optional[typing.Sequence["ListenerCondition"]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        '''(experimental) Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: (experimental) The protocol to use. Default: Determined from port if known
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group

        :stability: experimental
        '''
        props = AddApplicationTargetsProps(
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            port=port,
            protocol=protocol,
            protocol_version=protocol_version,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            stickiness_cookie_name=stickiness_cookie_name,
            target_group_name=target_group_name,
            targets=targets,
            conditions=conditions,
            priority=priority,
        )

        return typing.cast("ApplicationTargetGroup", jsii.invoke(self, "addTargets", [id, props]))

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: _Port_85922693,
    ) -> None:
        '''(experimental) Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerConnectable", [connectable, port_range]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplicationListener).__jsii_proxy_class__ = lambda : _IApplicationListenerProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget"
)
class IApplicationLoadBalancerTarget(typing_extensions.Protocol):
    '''(experimental) Interface for constructs that can be targets of an application load balancer.

    :stability: experimental
    '''

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        '''(experimental) Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -

        :stability: experimental
        '''
        ...


class _IApplicationLoadBalancerTargetProxy:
    '''(experimental) Interface for constructs that can be targets of an application load balancer.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget"

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: "IApplicationTargetGroup",
    ) -> "LoadBalancerTargetProps":
        '''(experimental) Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast("LoadBalancerTargetProps", jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplicationLoadBalancerTarget).__jsii_proxy_class__ = lambda : _IApplicationLoadBalancerTargetProxy


@jsii.interface(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IListenerAction")
class IListenerAction(typing_extensions.Protocol):
    '''(experimental) Interface for listener actions.

    :stability: experimental
    '''

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Render the actions in this chain.

        :stability: experimental
        '''
        ...


class _IListenerActionProxy:
    '''(experimental) Interface for listener actions.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IListenerAction"

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Render the actions in this chain.

        :stability: experimental
        '''
        return typing.cast(typing.List[CfnListener.ActionProperty], jsii.invoke(self, "renderActions", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IListenerAction).__jsii_proxy_class__ = lambda : _IListenerActionProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IListenerCertificate"
)
class IListenerCertificate(typing_extensions.Protocol):
    '''(experimental) A certificate source for an ELBv2 listener.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''(experimental) The ARN of the certificate to use.

        :stability: experimental
        '''
        ...


class _IListenerCertificateProxy:
    '''(experimental) A certificate source for an ELBv2 listener.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IListenerCertificate"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''(experimental) The ARN of the certificate to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IListenerCertificate).__jsii_proxy_class__ = lambda : _IListenerCertificateProxy


@jsii.interface(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ILoadBalancerV2")
class ILoadBalancerV2(_IResource_c80c4260, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The canonical hosted zone ID of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        '''(experimental) The DNS name of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        '''
        ...


class _ILoadBalancerV2Proxy(
    jsii.proxy_for(_IResource_c80c4260) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.ILoadBalancerV2"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerCanonicalHostedZoneId")
    def load_balancer_canonical_hosted_zone_id(self) -> builtins.str:
        '''(experimental) The canonical hosted zone ID of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            Z2P70J7EXAMPLE
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerCanonicalHostedZoneId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        '''(experimental) The DNS name of this load balancer.

        :stability: experimental
        :attribute: true

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            my - load - balancer - 424835706.us - west - 2.elb.amazonaws.com
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerDnsName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILoadBalancerV2).__jsii_proxy_class__ = lambda : _ILoadBalancerV2Proxy


@jsii.interface(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.INetworkListener")
class INetworkListener(_IResource_c80c4260, typing_extensions.Protocol):
    '''(experimental) Properties to reference an existing listener.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        ...


class _INetworkListenerProxy(
    jsii.proxy_for(_IResource_c80c4260) # type: ignore[misc]
):
    '''(experimental) Properties to reference an existing listener.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.INetworkListener"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''(experimental) ARN of the listener.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INetworkListener).__jsii_proxy_class__ = lambda : _INetworkListenerProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.INetworkLoadBalancer"
)
class INetworkLoadBalancer(
    ILoadBalancerV2,
    _IVpcEndpointServiceLoadBalancer_34cbc6e3,
    typing_extensions.Protocol,
):
    '''(experimental) A network load balancer.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC this load balancer has been created in (if available).

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> "NetworkListener":
        '''(experimental) Add a listener to this load balancer.

        :param id: -
        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener

        :stability: experimental
        '''
        ...


class _INetworkLoadBalancerProxy(
    jsii.proxy_for(ILoadBalancerV2), # type: ignore[misc]
    jsii.proxy_for(_IVpcEndpointServiceLoadBalancer_34cbc6e3), # type: ignore[misc]
):
    '''(experimental) A network load balancer.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.INetworkLoadBalancer"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC this load balancer has been created in (if available).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IVpc_f30d5663], jsii.get(self, "vpc"))

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> "NetworkListener":
        '''(experimental) Add a listener to this load balancer.

        :param id: -
        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener

        :stability: experimental
        '''
        props = BaseNetworkListenerProps(
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return typing.cast("NetworkListener", jsii.invoke(self, "addListener", [id, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INetworkLoadBalancer).__jsii_proxy_class__ = lambda : _INetworkLoadBalancerProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget"
)
class INetworkLoadBalancerTarget(typing_extensions.Protocol):
    '''(experimental) Interface for constructs that can be targets of an network load balancer.

    :stability: experimental
    '''

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        '''(experimental) Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -

        :stability: experimental
        '''
        ...


class _INetworkLoadBalancerTargetProxy:
    '''(experimental) Interface for constructs that can be targets of an network load balancer.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget"

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: "INetworkTargetGroup",
    ) -> "LoadBalancerTargetProps":
        '''(experimental) Attach load-balanced target to a TargetGroup.

        May return JSON to directly add to the [Targets] list, or return undefined
        if the target will register itself with the load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast("LoadBalancerTargetProps", jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INetworkLoadBalancerTarget).__jsii_proxy_class__ = lambda : _INetworkLoadBalancerTargetProxy


@jsii.interface(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ITargetGroup")
class ITargetGroup(constructs.IConstruct, typing_extensions.Protocol):
    '''(experimental) A target group.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        '''(experimental) A token representing a list of ARNs of the load balancers that route traffic to this target group.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> constructs.IDependable:
        '''(experimental) Return an object to depend on the listeners added to this target group.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) ARN of the target group.

        :stability: experimental
        '''
        ...


class _ITargetGroupProxy(
    jsii.proxy_for(constructs.IConstruct) # type: ignore[misc]
):
    '''(experimental) A target group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.ITargetGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        '''(experimental) A token representing a list of ARNs of the load balancers that route traffic to this target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> constructs.IDependable:
        '''(experimental) Return an object to depend on the listeners added to this target group.

        :stability: experimental
        '''
        return typing.cast(constructs.IDependable, jsii.get(self, "loadBalancerAttached"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) ARN of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITargetGroup).__jsii_proxy_class__ = lambda : _ITargetGroupProxy


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IpAddressType")
class IpAddressType(enum.Enum):
    '''(experimental) What kind of addresses to allocate to the load balancer.

    :stability: experimental
    '''

    IPV4 = "IPV4"
    '''(experimental) Allocate IPv4 addresses.

    :stability: experimental
    '''
    DUAL_STACK = "DUAL_STACK"
    '''(experimental) Allocate both IPv4 and IPv6 addresses.

    :stability: experimental
    '''


@jsii.implements(IListenerAction)
class ListenerAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ListenerAction",
):
    '''(experimental) What to do when a client makes a request to a listener.

    Some actions can be combined with other ones (specifically,
    you can perform authentication before serving the request).

    Multiple actions form a linked chain; the chain must always terminate in a
    *(weighted)forward*, *fixedResponse* or *redirect* action.

    If an action supports chaining, the next action can be indicated
    by passing it in the ``next`` property.

    (Called ``ListenerAction`` instead of the more strictly correct
    ``ListenerAction`` because this is the class most users interact
    with, and we want to make it not too visually overwhelming).

    :stability: experimental
    '''

    def __init__(
        self,
        action_json: CfnListener.ActionProperty,
        next: typing.Optional["ListenerAction"] = None,
    ) -> None:
        '''(experimental) Create an instance of ListenerAction.

        The default class should be good enough for most cases and
        should be created by using one of the static factory functions,
        but allow overriding to make sure we allow flexibility for the future.

        :param action_json: -
        :param next: -

        :stability: experimental
        '''
        jsii.create(ListenerAction, self, [action_json, next])

    @jsii.member(jsii_name="authenticateOidc") # type: ignore[misc]
    @builtins.classmethod
    def authenticate_oidc(
        cls,
        *,
        authorization_endpoint: builtins.str,
        client_id: builtins.str,
        client_secret: _SecretValue_3dd0ddae,
        issuer: builtins.str,
        next: "ListenerAction",
        token_endpoint: builtins.str,
        user_info_endpoint: builtins.str,
        authentication_request_extra_params: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_unauthenticated_request: typing.Optional["UnauthenticatedAction"] = None,
        scope: typing.Optional[builtins.str] = None,
        session_cookie_name: typing.Optional[builtins.str] = None,
        session_timeout: typing.Optional[_Duration_4839e8c3] = None,
    ) -> "ListenerAction":
        '''(experimental) Authenticate using an identity provider (IdP) that is compliant with OpenID Connect (OIDC).

        :param authorization_endpoint: (experimental) The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param client_id: (experimental) The OAuth 2.0 client identifier.
        :param client_secret: (experimental) The OAuth 2.0 client secret.
        :param issuer: (experimental) The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param next: (experimental) What action to execute next.
        :param token_endpoint: (experimental) The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param user_info_endpoint: (experimental) The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
        :param authentication_request_extra_params: (experimental) The query parameters (up to 10) to include in the redirect request to the authorization endpoint. Default: - No extra parameters
        :param on_unauthenticated_request: (experimental) The behavior if the user is not authenticated. Default: UnauthenticatedAction.AUTHENTICATE
        :param scope: (experimental) The set of user claims to be requested from the IdP. To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP. Default: "openid"
        :param session_cookie_name: (experimental) The name of the cookie used to maintain session information. Default: "AWSELBAuthSessionCookie"
        :param session_timeout: (experimental) The maximum duration of the authentication session. Default: Duration.days(7)

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html#oidc-requirements
        :stability: experimental
        '''
        options = AuthenticateOidcOptions(
            authorization_endpoint=authorization_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            issuer=issuer,
            next=next,
            token_endpoint=token_endpoint,
            user_info_endpoint=user_info_endpoint,
            authentication_request_extra_params=authentication_request_extra_params,
            on_unauthenticated_request=on_unauthenticated_request,
            scope=scope,
            session_cookie_name=session_cookie_name,
            session_timeout=session_timeout,
        )

        return typing.cast("ListenerAction", jsii.sinvoke(cls, "authenticateOidc", [options]))

    @jsii.member(jsii_name="fixedResponse") # type: ignore[misc]
    @builtins.classmethod
    def fixed_response(
        cls,
        status_code: jsii.Number,
        *,
        content_type: typing.Optional[builtins.str] = None,
        message_body: typing.Optional[builtins.str] = None,
    ) -> "ListenerAction":
        '''(experimental) Return a fixed response.

        :param status_code: -
        :param content_type: (experimental) Content Type of the response. Valid Values: text/plain | text/css | text/html | application/javascript | application/json Default: - Automatically determined
        :param message_body: (experimental) The response body. Default: - No body

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#fixed-response-actions
        :stability: experimental
        '''
        options = FixedResponseOptions(
            content_type=content_type, message_body=message_body
        )

        return typing.cast("ListenerAction", jsii.sinvoke(cls, "fixedResponse", [status_code, options]))

    @jsii.member(jsii_name="forward") # type: ignore[misc]
    @builtins.classmethod
    def forward(
        cls,
        target_groups: typing.Sequence["IApplicationTargetGroup"],
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> "ListenerAction":
        '''(experimental) Forward to one or more Target Groups.

        :param target_groups: -
        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#forward-actions
        :stability: experimental
        '''
        options = ForwardOptions(stickiness_duration=stickiness_duration)

        return typing.cast("ListenerAction", jsii.sinvoke(cls, "forward", [target_groups, options]))

    @jsii.member(jsii_name="redirect") # type: ignore[misc]
    @builtins.classmethod
    def redirect(
        cls,
        *,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[builtins.bool] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> "ListenerAction":
        '''(experimental) Redirect to a different URI.

        A URI consists of the following components:
        protocol://hostname:port/path?query. You must modify at least one of the
        following components to avoid a redirect loop: protocol, hostname, port, or
        path. Any components that you do not modify retain their original values.

        You can reuse URI components using the following reserved keywords:

        - ``#{protocol}``
        - ``#{host}``
        - ``#{port}``
        - ``#{path}`` (the leading "/" is removed)
        - ``#{query}``

        For example, you can change the path to "/new/#{path}", the hostname to
        "example.#{host}", or the query to "#{query}&value=xyz".

        :param host: (experimental) The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: - No change
        :param path: (experimental) The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: - No change
        :param permanent: (experimental) The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302). Default: false
        :param port: (experimental) The port. You can specify a value from 1 to 65535 or #{port}. Default: - No change
        :param protocol: (experimental) The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: - No change
        :param query: (experimental) The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: - No change

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#redirect-actions
        :stability: experimental
        '''
        options = RedirectOptions(
            host=host,
            path=path,
            permanent=permanent,
            port=port,
            protocol=protocol,
            query=query,
        )

        return typing.cast("ListenerAction", jsii.sinvoke(cls, "redirect", [options]))

    @jsii.member(jsii_name="weightedForward") # type: ignore[misc]
    @builtins.classmethod
    def weighted_forward(
        cls,
        target_groups: typing.Sequence["WeightedTargetGroup"],
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> "ListenerAction":
        '''(experimental) Forward to one or more Target Groups which are weighted differently.

        :param target_groups: -
        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#forward-actions
        :stability: experimental
        '''
        options = ForwardOptions(stickiness_duration=stickiness_duration)

        return typing.cast("ListenerAction", jsii.sinvoke(cls, "weightedForward", [target_groups, options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: constructs.Construct,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        '''(experimental) Called when the action is being used in a listener.

        :param scope: -
        :param listener: -
        :param associating_construct: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [scope, listener, associating_construct]))

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Render the actions in this chain.

        :stability: experimental
        '''
        return typing.cast(typing.List[CfnListener.ActionProperty], jsii.invoke(self, "renderActions", []))

    @jsii.member(jsii_name="renumber")
    def _renumber(
        self,
        actions: typing.Sequence[CfnListener.ActionProperty],
    ) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Renumber the "order" fields in the actions array.

        We don't number for 0 or 1 elements, but otherwise number them 1...#actions
        so ELB knows about the right order.

        Do this in ``ListenerAction`` instead of in ``Listener`` so that we give
        users the opportunity to override by subclassing and overriding ``renderActions``.

        :param actions: -

        :stability: experimental
        '''
        return typing.cast(typing.List[CfnListener.ActionProperty], jsii.invoke(self, "renumber", [actions]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="next")
    def _next(self) -> typing.Optional["ListenerAction"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ListenerAction"], jsii.get(self, "next"))


@jsii.implements(IListenerCertificate)
class ListenerCertificate(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ListenerCertificate",
):
    '''(experimental) A certificate source for an ELBv2 listener.

    :stability: experimental
    '''

    def __init__(self, certificate_arn: builtins.str) -> None:
        '''
        :param certificate_arn: -

        :stability: experimental
        '''
        jsii.create(ListenerCertificate, self, [certificate_arn])

    @jsii.member(jsii_name="fromArn") # type: ignore[misc]
    @builtins.classmethod
    def from_arn(cls, certificate_arn: builtins.str) -> "ListenerCertificate":
        '''(experimental) Use any certificate, identified by its ARN, as a listener certificate.

        :param certificate_arn: -

        :stability: experimental
        '''
        return typing.cast("ListenerCertificate", jsii.sinvoke(cls, "fromArn", [certificate_arn]))

    @jsii.member(jsii_name="fromCertificateManager") # type: ignore[misc]
    @builtins.classmethod
    def from_certificate_manager(
        cls,
        acm_certificate: _ICertificate_c194c70b,
    ) -> "ListenerCertificate":
        '''(experimental) Use an ACM certificate as a listener certificate.

        :param acm_certificate: -

        :stability: experimental
        '''
        return typing.cast("ListenerCertificate", jsii.sinvoke(cls, "fromCertificateManager", [acm_certificate]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''(experimental) The ARN of the certificate to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))


class ListenerCondition(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ListenerCondition",
):
    '''(experimental) ListenerCondition providers definition.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(ListenerCondition, self, [])

    @jsii.member(jsii_name="hostHeaders") # type: ignore[misc]
    @builtins.classmethod
    def host_headers(cls, values: typing.Sequence[builtins.str]) -> "ListenerCondition":
        '''(experimental) Create a host-header listener rule condition.

        :param values: Hosts for host headers.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "hostHeaders", [values]))

    @jsii.member(jsii_name="httpHeader") # type: ignore[misc]
    @builtins.classmethod
    def http_header(
        cls,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> "ListenerCondition":
        '''(experimental) Create a http-header listener rule condition.

        :param name: HTTP header name.
        :param values: HTTP header values.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "httpHeader", [name, values]))

    @jsii.member(jsii_name="httpRequestMethods") # type: ignore[misc]
    @builtins.classmethod
    def http_request_methods(
        cls,
        values: typing.Sequence[builtins.str],
    ) -> "ListenerCondition":
        '''(experimental) Create a http-request-method listener rule condition.

        :param values: HTTP request methods.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "httpRequestMethods", [values]))

    @jsii.member(jsii_name="pathPatterns") # type: ignore[misc]
    @builtins.classmethod
    def path_patterns(
        cls,
        values: typing.Sequence[builtins.str],
    ) -> "ListenerCondition":
        '''(experimental) Create a path-pattern listener rule condition.

        :param values: Path patterns.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "pathPatterns", [values]))

    @jsii.member(jsii_name="queryStrings") # type: ignore[misc]
    @builtins.classmethod
    def query_strings(
        cls,
        values: typing.Sequence["QueryStringCondition"],
    ) -> "ListenerCondition":
        '''(experimental) Create a query-string listener rule condition.

        :param values: Query string key/value pairs.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "queryStrings", [values]))

    @jsii.member(jsii_name="sourceIps") # type: ignore[misc]
    @builtins.classmethod
    def source_ips(cls, values: typing.Sequence[builtins.str]) -> "ListenerCondition":
        '''(experimental) Create a source-ip listener rule condition.

        :param values: Source ips.

        :stability: experimental
        '''
        return typing.cast("ListenerCondition", jsii.sinvoke(cls, "sourceIps", [values]))

    @jsii.member(jsii_name="renderRawCondition") # type: ignore[misc]
    @abc.abstractmethod
    def render_raw_condition(self) -> typing.Any:
        '''(experimental) Render the raw Cfn listener rule condition object.

        :stability: experimental
        '''
        ...


class _ListenerConditionProxy(ListenerCondition):
    @jsii.member(jsii_name="renderRawCondition")
    def render_raw_condition(self) -> typing.Any:
        '''(experimental) Render the raw Cfn listener rule condition object.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "renderRawCondition", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ListenerCondition).__jsii_proxy_class__ = lambda : _ListenerConditionProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.LoadBalancerTargetProps",
    jsii_struct_bases=[],
    name_mapping={"target_type": "targetType", "target_json": "targetJson"},
)
class LoadBalancerTargetProps:
    def __init__(
        self,
        *,
        target_type: "TargetType",
        target_json: typing.Any = None,
    ) -> None:
        '''(experimental) Result of attaching a target to load balancer.

        :param target_type: (experimental) What kind of target this is.
        :param target_json: (experimental) JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_type": target_type,
        }
        if target_json is not None:
            self._values["target_json"] = target_json

    @builtins.property
    def target_type(self) -> "TargetType":
        '''(experimental) What kind of target this is.

        :stability: experimental
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast("TargetType", result)

    @builtins.property
    def target_json(self) -> typing.Any:
        '''(experimental) JSON representing the target's direct addition to the TargetGroup list.

        May be omitted if the target is going to register itself later.

        :stability: experimental
        '''
        result = self._values.get("target_json")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkForwardOptions",
    jsii_struct_bases=[],
    name_mapping={"stickiness_duration": "stickinessDuration"},
)
class NetworkForwardOptions:
    def __init__(
        self,
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> None:
        '''(experimental) Options for ``NetworkListenerAction.forward()``.

        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if stickiness_duration is not None:
            self._values["stickiness_duration"] = stickiness_duration

    @builtins.property
    def stickiness_duration(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) For how long clients should be directed to the same target group.

        Range between 1 second and 7 days.

        :default: - No stickiness

        :stability: experimental
        '''
        result = self._values.get("stickiness_duration")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkForwardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INetworkListener)
class NetworkListener(
    BaseListener,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkListener",
):
    '''(experimental) Define a Network Listener.

    :stability: experimental
    :resource: AWS::ElasticLoadBalancingV2::Listener
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer: INetworkLoadBalancer,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional["NetworkListenerAction"] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param load_balancer: (experimental) The load balancer to attach this listener to.
        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.

        :stability: experimental
        '''
        props = NetworkListenerProps(
            load_balancer=load_balancer,
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(NetworkListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromLookup") # type: ignore[misc]
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_protocol: typing.Optional["Protocol"] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> INetworkListener:
        '''(experimental) Looks up a network listener.

        :param scope: -
        :param id: -
        :param listener_protocol: (experimental) Protocol of the listener port. Default: - listener is not filtered by protocol
        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: (experimental) Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: (experimental) Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags

        :stability: experimental
        '''
        options = NetworkListenerLookupOptions(
            listener_protocol=listener_protocol,
            listener_port=listener_port,
            load_balancer_arn=load_balancer_arn,
            load_balancer_tags=load_balancer_tags,
        )

        return typing.cast(INetworkListener, jsii.sinvoke(cls, "fromLookup", [scope, id, options]))

    @jsii.member(jsii_name="fromNetworkListenerArn") # type: ignore[misc]
    @builtins.classmethod
    def from_network_listener_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        network_listener_arn: builtins.str,
    ) -> INetworkListener:
        '''(experimental) Import an existing listener.

        :param scope: -
        :param id: -
        :param network_listener_arn: -

        :stability: experimental
        '''
        return typing.cast(INetworkListener, jsii.sinvoke(cls, "fromNetworkListenerArn", [scope, id, network_listener_arn]))

    @jsii.member(jsii_name="addAction")
    def add_action(self, _id: builtins.str, *, action: "NetworkListenerAction") -> None:
        '''(experimental) Perform the given Action on incoming requests.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        :param _id: -
        :param action: (experimental) Action to perform.

        :stability: experimental
        '''
        props = AddNetworkActionProps(action=action)

        return typing.cast(None, jsii.invoke(self, "addAction", [_id, props]))

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        _id: builtins.str,
        *target_groups: "INetworkTargetGroup",
    ) -> None:
        '''(experimental) Load balance incoming requests to the given target groups.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use ``addAction()``.

        :param _id: -
        :param target_groups: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addTargetGroups", [_id, *target_groups]))

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[INetworkLoadBalancerTarget]] = None,
    ) -> "NetworkTargetGroup":
        '''(experimental) Load balance incoming requests to the given load balancing targets.

        This method implicitly creates a NetworkTargetGroup for the targets
        involved, and a 'forward' action to route traffic to the given TargetGroup.

        If you want more control over the precise setup, create the TargetGroup
        and use ``addAction`` yourself.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param preserve_client_ip: (experimental) Indicates whether client IP preservation is enabled. Default: false if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, true.
        :param protocol: (experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - inherits the protocol of the listener
        :param proxy_protocol_v2: (experimental) Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type.

        :return: The newly created target group

        :stability: experimental
        '''
        props = AddNetworkTargetsProps(
            port=port,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            preserve_client_ip=preserve_client_ip,
            protocol=protocol,
            proxy_protocol_v2=proxy_protocol_v2,
            target_group_name=target_group_name,
            targets=targets,
        )

        return typing.cast("NetworkTargetGroup", jsii.invoke(self, "addTargets", [id, props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> INetworkLoadBalancer:
        '''(experimental) The load balancer this listener is attached to.

        :stability: experimental
        '''
        return typing.cast(INetworkLoadBalancer, jsii.get(self, "loadBalancer"))


@jsii.implements(IListenerAction)
class NetworkListenerAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkListenerAction",
):
    '''(experimental) What to do when a client makes a request to a listener.

    Some actions can be combined with other ones (specifically,
    you can perform authentication before serving the request).

    Multiple actions form a linked chain; the chain must always terminate in a
    *(weighted)forward*, *fixedResponse* or *redirect* action.

    If an action supports chaining, the next action can be indicated
    by passing it in the ``next`` property.

    :stability: experimental
    '''

    def __init__(
        self,
        action_json: CfnListener.ActionProperty,
        next: typing.Optional["NetworkListenerAction"] = None,
    ) -> None:
        '''(experimental) Create an instance of NetworkListenerAction.

        The default class should be good enough for most cases and
        should be created by using one of the static factory functions,
        but allow overriding to make sure we allow flexibility for the future.

        :param action_json: -
        :param next: -

        :stability: experimental
        '''
        jsii.create(NetworkListenerAction, self, [action_json, next])

    @jsii.member(jsii_name="forward") # type: ignore[misc]
    @builtins.classmethod
    def forward(
        cls,
        target_groups: typing.Sequence["INetworkTargetGroup"],
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> "NetworkListenerAction":
        '''(experimental) Forward to one or more Target Groups.

        :param target_groups: -
        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :stability: experimental
        '''
        options = NetworkForwardOptions(stickiness_duration=stickiness_duration)

        return typing.cast("NetworkListenerAction", jsii.sinvoke(cls, "forward", [target_groups, options]))

    @jsii.member(jsii_name="weightedForward") # type: ignore[misc]
    @builtins.classmethod
    def weighted_forward(
        cls,
        target_groups: typing.Sequence["NetworkWeightedTargetGroup"],
        *,
        stickiness_duration: typing.Optional[_Duration_4839e8c3] = None,
    ) -> "NetworkListenerAction":
        '''(experimental) Forward to one or more Target Groups which are weighted differently.

        :param target_groups: -
        :param stickiness_duration: (experimental) For how long clients should be directed to the same target group. Range between 1 second and 7 days. Default: - No stickiness

        :stability: experimental
        '''
        options = NetworkForwardOptions(stickiness_duration=stickiness_duration)

        return typing.cast("NetworkListenerAction", jsii.sinvoke(cls, "weightedForward", [target_groups, options]))

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.Construct, listener: INetworkListener) -> None:
        '''(experimental) Called when the action is being used in a listener.

        :param scope: -
        :param listener: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [scope, listener]))

    @jsii.member(jsii_name="renderActions")
    def render_actions(self) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Render the actions in this chain.

        :stability: experimental
        '''
        return typing.cast(typing.List[CfnListener.ActionProperty], jsii.invoke(self, "renderActions", []))

    @jsii.member(jsii_name="renumber")
    def _renumber(
        self,
        actions: typing.Sequence[CfnListener.ActionProperty],
    ) -> typing.List[CfnListener.ActionProperty]:
        '''(experimental) Renumber the "order" fields in the actions array.

        We don't number for 0 or 1 elements, but otherwise number them 1...#actions
        so ELB knows about the right order.

        Do this in ``NetworkListenerAction`` instead of in ``Listener`` so that we give
        users the opportunity to override by subclassing and overriding ``renderActions``.

        :param actions: -

        :stability: experimental
        '''
        return typing.cast(typing.List[CfnListener.ActionProperty], jsii.invoke(self, "renumber", [actions]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="next")
    def _next(self) -> typing.Optional["NetworkListenerAction"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["NetworkListenerAction"], jsii.get(self, "next"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkListenerLookupOptions",
    jsii_struct_bases=[BaseListenerLookupOptions],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "listener_protocol": "listenerProtocol",
    },
)
class NetworkListenerLookupOptions(BaseListenerLookupOptions):
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        listener_protocol: typing.Optional["Protocol"] = None,
    ) -> None:
        '''(experimental) Options for looking up a network listener.

        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: (experimental) Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: (experimental) Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        :param listener_protocol: (experimental) Protocol of the listener port. Default: - listener is not filtered by protocol

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Filter listeners by listener port.

        :default: - does not filter by listener port

        :stability: experimental
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def listener_protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) Protocol of the listener port.

        :default: - listener is not filtered by protocol

        :stability: experimental
        '''
        result = self._values.get("listener_protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkListenerProps",
    jsii_struct_bases=[BaseNetworkListenerProps],
    name_mapping={
        "port": "port",
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
        "load_balancer": "loadBalancer",
    },
)
class NetworkListenerProps(BaseNetworkListenerProps):
    def __init__(
        self,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[NetworkListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
        load_balancer: INetworkLoadBalancer,
    ) -> None:
        '''(experimental) Properties for a Network Listener attached to a Load Balancer.

        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.
        :param load_balancer: (experimental) The load balancer to attach this listener to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
            "load_balancer": load_balancer,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The port on which the listener listens for requests.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[IListenerCertificate]]:
        '''(experimental) Certificate list of ACM cert ARNs.

        :default: - No certificates.

        :stability: experimental
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[IListenerCertificate]], result)

    @builtins.property
    def default_action(self) -> typing.Optional[NetworkListenerAction]:
        '''(experimental) Default action to take for requests to this listener.

        This allows full control of the default Action of the load balancer,
        including weighted forwarding. See the ``NetworkListenerAction`` class for
        all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[NetworkListenerAction], result)

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["INetworkTargetGroup"]]:
        '''(experimental) Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_target_groups")
        return typing.cast(typing.Optional[typing.List["INetworkTargetGroup"]], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TLS if certificates are provided. TCP otherwise.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional["SslPolicy"]:
        '''(experimental) SSL Policy.

        :default: - Current predefined security policy.

        :stability: experimental
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional["SslPolicy"], result)

    @builtins.property
    def load_balancer(self) -> INetworkLoadBalancer:
        '''(experimental) The load balancer to attach this listener to.

        :stability: experimental
        '''
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return typing.cast(INetworkLoadBalancer, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(INetworkLoadBalancer)
class NetworkLoadBalancer(
    BaseLoadBalancer,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkLoadBalancer",
):
    '''(experimental) Define a new network load balancer.

    :stability: experimental
    :resource: AWS::ElasticLoadBalancingV2::LoadBalancer
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cross_zone_enabled: typing.Optional[builtins.bool] = None,
        vpc: _IVpc_f30d5663,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_e57d76df] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cross_zone_enabled: (experimental) Indicates whether cross-zone load balancing is enabled. Default: false
        :param vpc: (experimental) The VPC network to place the load balancer in.
        :param deletion_protection: (experimental) Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: (experimental) Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: (experimental) Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: (experimental) Which subnets place the load balancer in. Default: - the Vpc default strategy.

        :stability: experimental
        '''
        props = NetworkLoadBalancerProps(
            cross_zone_enabled=cross_zone_enabled,
            vpc=vpc,
            deletion_protection=deletion_protection,
            internet_facing=internet_facing,
            load_balancer_name=load_balancer_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(NetworkLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromLookup") # type: ignore[misc]
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> INetworkLoadBalancer:
        '''(experimental) Looks up the network load balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        '''
        options = NetworkLoadBalancerLookupOptions(
            load_balancer_arn=load_balancer_arn, load_balancer_tags=load_balancer_tags
        )

        return typing.cast(INetworkLoadBalancer, jsii.sinvoke(cls, "fromLookup", [scope, id, options]))

    @jsii.member(jsii_name="fromNetworkLoadBalancerAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_network_load_balancer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> INetworkLoadBalancer:
        '''
        :param scope: -
        :param id: -
        :param load_balancer_arn: (experimental) ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: (experimental) The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: (experimental) The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param vpc: (experimental) The VPC to associate with the load balancer. Default: - When not provided, listeners cannot be created on imported load balancers.

        :stability: experimental
        '''
        attrs = NetworkLoadBalancerAttributes(
            load_balancer_arn=load_balancer_arn,
            load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id,
            load_balancer_dns_name=load_balancer_dns_name,
            vpc=vpc,
        )

        return typing.cast(INetworkLoadBalancer, jsii.sinvoke(cls, "fromNetworkLoadBalancerAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port: jsii.Number,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[NetworkListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["INetworkTargetGroup"]] = None,
        protocol: typing.Optional["Protocol"] = None,
        ssl_policy: typing.Optional["SslPolicy"] = None,
    ) -> NetworkListener:
        '''(experimental) Add a listener to this load balancer.

        :param id: -
        :param port: (experimental) The port on which the listener listens for requests.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default Action of the load balancer, including weighted forwarding. See the ``NetworkListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param protocol: (experimental) Protocol for listener, expects TCP, TLS, UDP, or TCP_UDP. Default: - TLS if certificates are provided. TCP otherwise.
        :param ssl_policy: (experimental) SSL Policy. Default: - Current predefined security policy.

        :return: The newly created listener

        :stability: experimental
        '''
        props = BaseNetworkListenerProps(
            port=port,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return typing.cast(NetworkListener, jsii.invoke(self, "addListener", [id, props]))

    @jsii.member(jsii_name="logAccessLogs")
    def log_access_logs(
        self,
        bucket: _IBucket_42e086fd,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Enable access logging for this load balancer.

        A region must be specified on the stack containing the load balancer; you cannot enable logging on
        environment-agnostic stacks. See https://docs.aws.amazon.com/cdk/latest/guide/environments.html

        This is extending the BaseLoadBalancer.logAccessLogs method to match the bucket permissions described
        at https://docs.aws.amazon.com/elasticloadbalancing/latest/network/load-balancer-access-logs.html#access-logging-bucket-requirements

        :param bucket: -
        :param prefix: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "logAccessLogs", [bucket, prefix]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) Return the given named metric for this Network Load Balancer.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricActiveFlowCount")
    def metric_active_flow_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of concurrent TCP flows (or connections) from clients to targets.

        This metric includes connections in the SYN_SENT and ESTABLISHED states.
        TCP connections are not terminated at the load balancer, so a client
        opening a TCP connection to a target counts as a single flow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricActiveFlowCount", [props]))

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricConsumedLCUs", [props]))

    @jsii.member(jsii_name="metricNewFlowCount")
    def metric_new_flow_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of new TCP flows (or connections) established from clients to targets in the time period.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricNewFlowCount", [props]))

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of bytes processed by the load balancer, including TCP/IP headers.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricProcessedBytes", [props]))

    @jsii.member(jsii_name="metricTcpClientResetCount")
    def metric_tcp_client_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of reset (RST) packets sent from a client to a target.

        These resets are generated by the client and forwarded by the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTcpClientResetCount", [props]))

    @jsii.member(jsii_name="metricTcpElbResetCount")
    def metric_tcp_elb_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of reset (RST) packets generated by the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTcpElbResetCount", [props]))

    @jsii.member(jsii_name="metricTcpTargetResetCount")
    def metric_tcp_target_reset_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of reset (RST) packets sent from a target to a client.

        These resets are generated by the target and forwarded by the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTcpTargetResetCount", [props]))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkLoadBalancerAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_canonical_hosted_zone_id": "loadBalancerCanonicalHostedZoneId",
        "load_balancer_dns_name": "loadBalancerDnsName",
        "vpc": "vpc",
    },
)
class NetworkLoadBalancerAttributes:
    def __init__(
        self,
        *,
        load_balancer_arn: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> None:
        '''(experimental) Properties to reference an existing load balancer.

        :param load_balancer_arn: (experimental) ARN of the load balancer.
        :param load_balancer_canonical_hosted_zone_id: (experimental) The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: (experimental) The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param vpc: (experimental) The VPC to associate with the load balancer. Default: - When not provided, listeners cannot be created on imported load balancers.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer_arn": load_balancer_arn,
        }
        if load_balancer_canonical_hosted_zone_id is not None:
            self._values["load_balancer_canonical_hosted_zone_id"] = load_balancer_canonical_hosted_zone_id
        if load_balancer_dns_name is not None:
            self._values["load_balancer_dns_name"] = load_balancer_dns_name
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) ARN of the load balancer.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        assert result is not None, "Required property 'load_balancer_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_canonical_hosted_zone_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The canonical hosted zone ID of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_canonical_hosted_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_dns_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS name of this load balancer.

        :default: - When not provided, LB cannot be used as Route53 Alias target.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_dns_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC to associate with the load balancer.

        :default:

        - When not provided, listeners cannot be created on imported load
        balancers.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_f30d5663], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkLoadBalancerLookupOptions",
    jsii_struct_bases=[BaseLoadBalancerLookupOptions],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class NetworkLoadBalancerLookupOptions(BaseLoadBalancerLookupOptions):
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for looking up an NetworkLoadBalancer.

        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkLoadBalancerProps",
    jsii_struct_bases=[BaseLoadBalancerProps],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
        "cross_zone_enabled": "crossZoneEnabled",
    },
)
class NetworkLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_f30d5663,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_e57d76df] = None,
        cross_zone_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for a network load balancer.

        :param vpc: (experimental) The VPC network to place the load balancer in.
        :param deletion_protection: (experimental) Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: (experimental) Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: (experimental) Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: (experimental) Which subnets place the load balancer in. Default: - the Vpc default strategy.
        :param cross_zone_enabled: (experimental) Indicates whether cross-zone load balancing is enabled. Default: false

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_e57d76df(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if cross_zone_enabled is not None:
            self._values["cross_zone_enabled"] = cross_zone_enabled

    @builtins.property
    def vpc(self) -> _IVpc_f30d5663:
        '''(experimental) The VPC network to place the load balancer in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_f30d5663, result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether deletion protection is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the load balancer has an internet-routable address.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the load balancer.

        :default: - Automatically generated name.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_e57d76df]:
        '''(experimental) Which subnets place the load balancer in.

        :default: - the Vpc default strategy.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_e57d76df], result)

    @builtins.property
    def cross_zone_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether cross-zone load balancing is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cross_zone_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkTargetGroupProps",
    jsii_struct_bases=[BaseTargetGroupProps],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
        "port": "port",
        "preserve_client_ip": "preserveClientIp",
        "protocol": "protocol",
        "proxy_protocol_v2": "proxyProtocolV2",
        "targets": "targets",
    },
)
class NetworkTargetGroupProps(BaseTargetGroupProps):
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional["TargetType"] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
        port: jsii.Number,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        protocol: typing.Optional["Protocol"] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        targets: typing.Optional[typing.Sequence[INetworkLoadBalancerTarget]] = None,
    ) -> None:
        '''(experimental) Properties for a new Network Target Group.

        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: (experimental) Health check configuration. Default: - None.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: (experimental) The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: (experimental) The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: (experimental) The port on which the listener listens for requests.
        :param preserve_client_ip: (experimental) Indicates whether client IP preservation is enabled. Default: false if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, true.
        :param protocol: (experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - TCP
        :param proxy_protocol_v2: (experimental) Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc
        if preserve_client_ip is not None:
            self._values["preserve_client_ip"] = preserve_client_ip
        if protocol is not None:
            self._values["protocol"] = protocol
        if proxy_protocol_v2 is not None:
            self._values["proxy_protocol_v2"] = proxy_protocol_v2
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) Health check configuration.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.

        :stability: experimental
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional["TargetType"]:
        '''(experimental) The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.

        :stability: experimental
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional["TargetType"], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_f30d5663], result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The port on which the listener listens for requests.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def preserve_client_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether client IP preservation is enabled.

        :default:

        false if the target group type is IP address and the
        target group protocol is TCP or TLS. Otherwise, true.

        :stability: experimental
        '''
        result = self._values.get("preserve_client_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def protocol(self) -> typing.Optional["Protocol"]:
        '''(experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP.

        :default: - TCP

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional["Protocol"], result)

    @builtins.property
    def proxy_protocol_v2(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether Proxy Protocol version 2 is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("proxy_protocol_v2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[INetworkLoadBalancerTarget]]:
        '''(experimental) The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :default: - No targets.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[INetworkLoadBalancerTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkWeightedTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "weight": "weight"},
)
class NetworkWeightedTargetGroup:
    def __init__(
        self,
        *,
        target_group: "INetworkTargetGroup",
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A Target Group and weight combination.

        :param target_group: (experimental) The target group.
        :param weight: (experimental) The target group's weight. Range is [0..1000). Default: 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_group": target_group,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def target_group(self) -> "INetworkTargetGroup":
        '''(experimental) The target group.

        :stability: experimental
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast("INetworkTargetGroup", result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The target group's weight.

        Range is [0..1000).

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkWeightedTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.Protocol")
class Protocol(enum.Enum):
    '''(experimental) Backend protocol for network load balancers and health checks.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) HTTP (ALB health checks and NLB health checks).

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) HTTPS (ALB health checks and NLB health checks).

    :stability: experimental
    '''
    TCP = "TCP"
    '''(experimental) TCP (NLB, NLB health checks).

    :stability: experimental
    '''
    TLS = "TLS"
    '''(experimental) TLS (NLB).

    :stability: experimental
    '''
    UDP = "UDP"
    '''(experimental) UDP (NLB).

    :stability: experimental
    '''
    TCP_UDP = "TCP_UDP"
    '''(experimental) Listen to both TCP and UDP on the same port (NLB).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.QueryStringCondition",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "key": "key"},
)
class QueryStringCondition:
    def __init__(
        self,
        *,
        value: builtins.str,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for the key/value pair of the query string.

        :param value: (experimental) The query string value for the condition.
        :param key: (experimental) The query string key for the condition. Default: - Any key can be matched.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The query string value for the condition.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The query string key for the condition.

        :default: - Any key can be matched.

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryStringCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.RedirectOptions",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "path": "path",
        "permanent": "permanent",
        "port": "port",
        "protocol": "protocol",
        "query": "query",
    },
)
class RedirectOptions:
    def __init__(
        self,
        *,
        host: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        permanent: typing.Optional[builtins.bool] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ``ListenerAction.redirect()``.

        A URI consists of the following components:
        protocol://hostname:port/path?query. You must modify at least one of the
        following components to avoid a redirect loop: protocol, hostname, port, or
        path. Any components that you do not modify retain their original values.

        You can reuse URI components using the following reserved keywords:

        - ``#{protocol}``
        - ``#{host}``
        - ``#{port}``
        - ``#{path}`` (the leading "/" is removed)
        - ``#{query}``

        For example, you can change the path to "/new/#{path}", the hostname to
        "example.#{host}", or the query to "#{query}&value=xyz".

        :param host: (experimental) The hostname. This component is not percent-encoded. The hostname can contain #{host}. Default: - No change
        :param path: (experimental) The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}. Default: - No change
        :param permanent: (experimental) The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302). Default: false
        :param port: (experimental) The port. You can specify a value from 1 to 65535 or #{port}. Default: - No change
        :param protocol: (experimental) The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP. Default: - No change
        :param query: (experimental) The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords. Default: - No change

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if host is not None:
            self._values["host"] = host
        if path is not None:
            self._values["path"] = path
        if permanent is not None:
            self._values["permanent"] = permanent
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hostname.

        This component is not percent-encoded. The hostname can contain #{host}.

        :default: - No change

        :stability: experimental
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The absolute path, starting with the leading "/".

        This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.

        :default: - No change

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permanent(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The HTTP redirect code.

        The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("permanent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def port(self) -> typing.Optional[builtins.str]:
        '''(experimental) The port.

        You can specify a value from 1 to 65535 or #{port}.

        :default: - No change

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''(experimental) The protocol.

        You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You cannot redirect HTTPS to HTTP.

        :default: - No change

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''(experimental) The query parameters, URL-encoded when necessary, but not percent-encoded.

        Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.

        :default: - No change

        :stability: experimental
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedirectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.SslPolicy")
class SslPolicy(enum.Enum):
    '''(experimental) Elastic Load Balancing provides the following security policies for Application Load Balancers.

    We recommend the Recommended policy for general use. You can
    use the ForwardSecrecy policy if you require Forward Secrecy
    (FS).

    You can use one of the TLS policies to meet compliance and security
    standards that require disabling certain TLS protocol versions, or to
    support legacy clients that require deprecated ciphers.

    :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html
    :stability: experimental
    '''

    RECOMMENDED = "RECOMMENDED"
    '''(experimental) The recommended security policy.

    :stability: experimental
    '''
    FORWARD_SECRECY_TLS12_RES_GCM = "FORWARD_SECRECY_TLS12_RES_GCM"
    '''(experimental) Strong foward secrecy ciphers and TLV1.2 only (2020 edition). Same as FORWARD_SECRECY_TLS12_RES, but only supports GCM versions of the TLS ciphers.

    :stability: experimental
    '''
    FORWARD_SECRECY_TLS12_RES = "FORWARD_SECRECY_TLS12_RES"
    '''(experimental) Strong forward secrecy ciphers and TLS1.2 only.

    :stability: experimental
    '''
    FORWARD_SECRECY_TLS12 = "FORWARD_SECRECY_TLS12"
    '''(experimental) Forward secrecy ciphers and TLS1.2 only.

    :stability: experimental
    '''
    FORWARD_SECRECY_TLS11 = "FORWARD_SECRECY_TLS11"
    '''(experimental) Forward secrecy ciphers only with TLS1.1 and higher.

    :stability: experimental
    '''
    FORWARD_SECRECY = "FORWARD_SECRECY"
    '''(experimental) Forward secrecy ciphers only.

    :stability: experimental
    '''
    TLS12 = "TLS12"
    '''(experimental) TLS1.2 only and no SHA ciphers.

    :stability: experimental
    '''
    TLS12_EXT = "TLS12_EXT"
    '''(experimental) TLS1.2 only with all ciphers.

    :stability: experimental
    '''
    TLS11 = "TLS11"
    '''(experimental) TLS1.1 and higher with all ciphers.

    :stability: experimental
    '''
    LEGACY = "LEGACY"
    '''(experimental) Support for DES-CBC3-SHA.

    Do not use this security policy unless you must support a legacy client
    that requires the DES-CBC3-SHA cipher, which is a weak cipher.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.TargetGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "target_group_arn": "targetGroupArn",
        "load_balancer_arns": "loadBalancerArns",
    },
)
class TargetGroupAttributes:
    def __init__(
        self,
        *,
        target_group_arn: builtins.str,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties to reference an existing target group.

        :param target_group_arn: (experimental) ARN of the target group.
        :param load_balancer_arns: (experimental) A Token representing the list of ARNs for the load balancer routing to this target group.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_group_arn": target_group_arn,
        }
        if load_balancer_arns is not None:
            self._values["load_balancer_arns"] = load_balancer_arns

    @builtins.property
    def target_group_arn(self) -> builtins.str:
        '''(experimental) ARN of the target group.

        :stability: experimental
        '''
        result = self._values.get("target_group_arn")
        assert result is not None, "Required property 'target_group_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_balancer_arns(self) -> typing.Optional[builtins.str]:
        '''(experimental) A Token representing the list of ARNs for the load balancer routing to this target group.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arns")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITargetGroup)
class TargetGroupBase(
    constructs.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.TargetGroupBase",
):
    '''(experimental) Define the target of a load balancer.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        base_props: BaseTargetGroupProps,
        additional_props: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param base_props: -
        :param additional_props: -

        :stability: experimental
        '''
        jsii.create(TargetGroupBase, self, [scope, id, base_props, additional_props])

    @jsii.member(jsii_name="addLoadBalancerTarget")
    def _add_load_balancer_target(
        self,
        *,
        target_type: "TargetType",
        target_json: typing.Any = None,
    ) -> None:
        '''(experimental) Register the given load balancing target as part of this group.

        :param target_type: (experimental) What kind of target this is.
        :param target_json: (experimental) JSON representing the target's direct addition to the TargetGroup list. May be omitted if the target is going to register itself later.

        :stability: experimental
        '''
        props = LoadBalancerTargetProps(
            target_type=target_type, target_json=target_json
        )

        return typing.cast(None, jsii.invoke(self, "addLoadBalancerTarget", [props]))

    @jsii.member(jsii_name="configureHealthCheck")
    def configure_health_check(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        healthy_grpc_codes: typing.Optional[builtins.str] = None,
        healthy_http_codes: typing.Optional[builtins.str] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_Duration_4839e8c3] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[Protocol] = None,
        timeout: typing.Optional[_Duration_4839e8c3] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Set/replace the target group's health check.

        :param enabled: (experimental) Indicates whether health checks are enabled. If the target type is lambda, health checks are disabled by default but can be enabled. If the target type is instance or ip, health checks are always enabled and cannot be disabled. Default: - Determined automatically.
        :param healthy_grpc_codes: (experimental) GRPC code to use when checking for a successful response from a target. You can specify values between 0 and 99. You can specify multiple values (for example, "0,1") or a range of values (for example, "0-5"). Default: - 12
        :param healthy_http_codes: (experimental) HTTP code to use when checking for a successful response from a target. For Application Load Balancers, you can specify values between 200 and 499, and the default value is 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").
        :param healthy_threshold_count: (experimental) The number of consecutive health checks successes required before considering an unhealthy target healthy. For Application Load Balancers, the default is 5. For Network Load Balancers, the default is 3. Default: 5 for ALBs, 3 for NLBs
        :param interval: (experimental) The approximate number of seconds between health checks for an individual target. Default: Duration.seconds(30)
        :param path: (experimental) The ping path destination where Elastic Load Balancing sends health check requests. Default: /
        :param port: (experimental) The port that the load balancer uses when performing health checks on the targets. Default: 'traffic-port'
        :param protocol: (experimental) The protocol the load balancer uses when performing health checks on targets. The TCP protocol is supported for health checks only if the protocol of the target group is TCP, TLS, UDP, or TCP_UDP. The TLS, UDP, and TCP_UDP protocols are not supported for health checks. Default: HTTP for ALBs, TCP for NLBs
        :param timeout: (experimental) The amount of time, in seconds, during which no response from a target means a failed health check. For Application Load Balancers, the range is 2-60 seconds and the default is 5 seconds. For Network Load Balancers, this is 10 seconds for TCP and HTTPS health checks and 6 seconds for HTTP health checks. Default: Duration.seconds(5) for ALBs, Duration.seconds(10) or Duration.seconds(6) for NLBs
        :param unhealthy_threshold_count: (experimental) The number of consecutive health check failures required before considering a target unhealthy. For Application Load Balancers, the default is 2. For Network Load Balancers, this value must be the same as the healthy threshold count. Default: 2

        :stability: experimental
        '''
        health_check = HealthCheck(
            enabled=enabled,
            healthy_grpc_codes=healthy_grpc_codes,
            healthy_http_codes=healthy_http_codes,
            healthy_threshold_count=healthy_threshold_count,
            interval=interval,
            path=path,
            port=port,
            protocol=protocol,
            timeout=timeout,
            unhealthy_threshold_count=unhealthy_threshold_count,
        )

        return typing.cast(None, jsii.invoke(self, "configureHealthCheck", [health_check]))

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Set a non-standard attribute on the target group.

        :param key: -
        :param value: -

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html#target-group-attributes
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "setAttribute", [key, value]))

    @jsii.member(jsii_name="validateTargetGroup")
    def _validate_target_group(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateTargetGroup", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="defaultPort")
    def _default_port(self) -> jsii.Number:
        '''(experimental) Default port configured for members of this target group.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "defaultPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    @abc.abstractmethod
    def first_load_balancer_full_name(self) -> builtins.str:
        '''(experimental) Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArns")
    def load_balancer_arns(self) -> builtins.str:
        '''(experimental) A token representing a list of ARNs of the load balancers that route traffic to this target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerAttached")
    def load_balancer_attached(self) -> constructs.IDependable:
        '''(experimental) List of constructs that need to be depended on to ensure the TargetGroup is associated to a load balancer.

        :stability: experimental
        '''
        return typing.cast(constructs.IDependable, jsii.get(self, "loadBalancerAttached"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerAttachedDependencies")
    def _load_balancer_attached_dependencies(self) -> constructs.DependencyGroup:
        '''(experimental) Configurable dependable with all resources that lead to load balancer attachment.

        :stability: experimental
        '''
        return typing.cast(constructs.DependencyGroup, jsii.get(self, "loadBalancerAttachedDependencies"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupArn")
    def target_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupFullName")
    def target_group_full_name(self) -> builtins.str:
        '''(experimental) The full name of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupFullName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupLoadBalancerArns")
    def target_group_load_balancer_arns(self) -> typing.List[builtins.str]:
        '''(experimental) ARNs of load balancers load balancing to this TargetGroup.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetGroupLoadBalancerArns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> builtins.str:
        '''(experimental) The name of the target group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> HealthCheck:
        '''
        :stability: experimental
        '''
        return typing.cast(HealthCheck, jsii.get(self, "healthCheck"))

    @health_check.setter
    def health_check(self, value: HealthCheck) -> None:
        jsii.set(self, "healthCheck", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targetType")
    def _target_type(self) -> typing.Optional["TargetType"]:
        '''(experimental) The types of the directly registered members of this target group.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["TargetType"], jsii.get(self, "targetType"))

    @_target_type.setter
    def _target_type(self, value: typing.Optional["TargetType"]) -> None:
        jsii.set(self, "targetType", value)


class _TargetGroupBaseProxy(TargetGroupBase):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        '''(experimental) Full name of first load balancer.

        This identifier is emitted as a dimensions of the metrics of this target
        group.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            app / my - load - balancer / 123456789
        '''
        return typing.cast(builtins.str, jsii.get(self, "firstLoadBalancerFullName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TargetGroupBase).__jsii_proxy_class__ = lambda : _TargetGroupBaseProxy


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.TargetType")
class TargetType(enum.Enum):
    '''(experimental) How to interpret the load balancing target identifiers.

    :stability: experimental
    '''

    INSTANCE = "INSTANCE"
    '''(experimental) Targets identified by instance ID.

    :stability: experimental
    '''
    IP = "IP"
    '''(experimental) Targets identified by IP address.

    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''(experimental) Target is a single Lambda Function.

    :stability: experimental
    '''


@jsii.enum(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.UnauthenticatedAction")
class UnauthenticatedAction(enum.Enum):
    '''(experimental) What to do with unauthenticated requests.

    :stability: experimental
    '''

    DENY = "DENY"
    '''(experimental) Return an HTTP 401 Unauthorized error.

    :stability: experimental
    '''
    ALLOW = "ALLOW"
    '''(experimental) Allow the request to be forwarded to the target.

    :stability: experimental
    '''
    AUTHENTICATE = "AUTHENTICATE"
    '''(experimental) Redirect the request to the IdP authorization endpoint.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.WeightedTargetGroup",
    jsii_struct_bases=[],
    name_mapping={"target_group": "targetGroup", "weight": "weight"},
)
class WeightedTargetGroup:
    def __init__(
        self,
        *,
        target_group: "IApplicationTargetGroup",
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) A Target Group and weight combination.

        :param target_group: (experimental) The target group.
        :param weight: (experimental) The target group's weight. Range is [0..1000). Default: 1

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_group": target_group,
        }
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def target_group(self) -> "IApplicationTargetGroup":
        '''(experimental) The target group.

        :stability: experimental
        '''
        result = self._values.get("target_group")
        assert result is not None, "Required property 'target_group' is missing"
        return typing.cast("IApplicationTargetGroup", result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The target group's weight.

        Range is [0..1000).

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WeightedTargetGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddApplicationActionProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "priority": "priority",
        "action": "action",
    },
)
class AddApplicationActionProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
        action: ListenerAction,
    ) -> None:
        '''(experimental) Properties for adding a new action to a listener.

        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param action: (experimental) Action to perform.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[ListenerCondition]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def action(self) -> ListenerAction:
        '''(experimental) Action to perform.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(ListenerAction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddApplicationTargetGroupsProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "priority": "priority",
        "target_groups": "targetGroups",
    },
)
class AddApplicationTargetGroupsProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
        target_groups: typing.Sequence["IApplicationTargetGroup"],
    ) -> None:
        '''(experimental) Properties for adding a new target group to a listener.

        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param target_groups: (experimental) Target groups to forward requests to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_groups": target_groups,
        }
        if conditions is not None:
            self._values["conditions"] = conditions
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[ListenerCondition]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_groups(self) -> typing.List["IApplicationTargetGroup"]:
        '''(experimental) Target groups to forward requests to.

        :stability: experimental
        '''
        result = self._values.get("target_groups")
        assert result is not None, "Required property 'target_groups' is missing"
        return typing.cast(typing.List["IApplicationTargetGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationTargetGroupsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.AddApplicationTargetsProps",
    jsii_struct_bases=[AddRuleProps],
    name_mapping={
        "conditions": "conditions",
        "priority": "priority",
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "stickiness_cookie_name": "stickinessCookieName",
        "target_group_name": "targetGroupName",
        "targets": "targets",
    },
)
class AddApplicationTargetsProps(AddRuleProps):
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[IApplicationLoadBalancerTarget]] = None,
    ) -> None:
        '''(experimental) Properties for adding new targets to a listener.

        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: (experimental) The protocol to use. Default: Determined from port if known
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if priority is not None:
            self._values["priority"] = priority
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if stickiness_cookie_name is not None:
            self._values["stickiness_cookie_name"] = stickiness_cookie_name
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[ListenerCondition]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) Health check configuration.

        :default: No health check

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port on which the listener listens for requests.

        :default: Determined from protocol if known

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        '''(experimental) The protocol to use.

        :default: Determined from port if known

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ApplicationProtocol], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[ApplicationProtocolVersion]:
        '''(experimental) The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1

        :stability: experimental
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[ApplicationProtocolVersion], result)

    @builtins.property
    def slow_start(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("slow_start")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        :default: Stickiness disabled

        :stability: experimental
        '''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def stickiness_cookie_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of an application-based stickiness cookie.

        Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP,
        and AWSALBTG; they're reserved for use by the load balancer.

        Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter.
        If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted.

        :default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html
        :stability: experimental
        '''
        result = self._values.get("stickiness_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: Automatically generated

        :stability: experimental
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IApplicationLoadBalancerTarget]]:
        '''(experimental) The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. All target must be of the same type.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[IApplicationLoadBalancerTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddApplicationTargetsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApplicationListener)
class ApplicationListener(
    BaseListener,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListener",
):
    '''(experimental) Define an ApplicationListener.

    :stability: experimental
    :resource: AWS::ElasticLoadBalancingV2::Listener
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer: "IApplicationLoadBalancer",
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param load_balancer: (experimental) The load balancer to attach this listener to.
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.

        :stability: experimental
        '''
        props = ApplicationListenerProps(
            load_balancer=load_balancer,
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        jsii.create(ApplicationListener, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationListenerAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_application_listener_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_arn: builtins.str,
        default_port: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_ISecurityGroup_acf8a799] = None,
    ) -> IApplicationListener:
        '''(experimental) Import an existing listener.

        :param scope: -
        :param id: -
        :param listener_arn: (experimental) ARN of the listener.
        :param default_port: (experimental) The default port on which this listener is listening.
        :param security_group: (experimental) Security group of the load balancer this listener is associated with.

        :stability: experimental
        '''
        attrs = ApplicationListenerAttributes(
            listener_arn=listener_arn,
            default_port=default_port,
            security_group=security_group,
        )

        return typing.cast(IApplicationListener, jsii.sinvoke(cls, "fromApplicationListenerAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromLookup") # type: ignore[misc]
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_protocol: typing.Optional[ApplicationProtocol] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> IApplicationListener:
        '''(experimental) Look up an ApplicationListener.

        :param scope: -
        :param id: -
        :param listener_arn: (experimental) ARN of the listener to look up. Default: - does not filter by listener arn
        :param listener_protocol: (experimental) Filter listeners by listener protocol. Default: - does not filter by listener protocol
        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: (experimental) Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: (experimental) Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags

        :stability: experimental
        '''
        options = ApplicationListenerLookupOptions(
            listener_arn=listener_arn,
            listener_protocol=listener_protocol,
            listener_port=listener_port,
            load_balancer_arn=load_balancer_arn,
            load_balancer_tags=load_balancer_tags,
        )

        return typing.cast(IApplicationListener, jsii.sinvoke(cls, "fromLookup", [scope, id, options]))

    @jsii.member(jsii_name="addAction")
    def add_action(
        self,
        id: builtins.str,
        *,
        action: ListenerAction,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Perform the given default action on incoming requests.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses. See
        the ``ListenerAction`` class for all options.

        It's possible to add routing conditions to the Action added in this way.
        At least one Action must be added without conditions (which becomes the
        default Action).

        :param id: -
        :param action: (experimental) Action to perform.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :stability: experimental
        '''
        props = AddApplicationActionProps(
            action=action, conditions=conditions, priority=priority
        )

        return typing.cast(None, jsii.invoke(self, "addAction", [id, props]))

    @jsii.member(jsii_name="addCertificates")
    def add_certificates(
        self,
        id: builtins.str,
        certificates: typing.Sequence[IListenerCertificate],
    ) -> None:
        '''(experimental) Add one or more certificates to this listener.

        After the first certificate, this creates ApplicationListenerCertificates
        resources since cloudformation requires the certificates array on the
        listener resource to have a length of 1.

        :param id: -
        :param certificates: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addCertificates", [id, certificates]))

    @jsii.member(jsii_name="addTargetGroups")
    def add_target_groups(
        self,
        id: builtins.str,
        *,
        target_groups: typing.Sequence["IApplicationTargetGroup"],
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Load balance incoming requests to the given target groups.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use ``addAction()``.

        It's possible to add routing conditions to the TargetGroups added in this
        way. At least one TargetGroup must be added without conditions (which will
        become the default Action for this listener).

        :param id: -
        :param target_groups: (experimental) Target groups to forward requests to.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :stability: experimental
        '''
        props = AddApplicationTargetGroupsProps(
            target_groups=target_groups, conditions=conditions, priority=priority
        )

        return typing.cast(None, jsii.invoke(self, "addTargetGroups", [id, props]))

    @jsii.member(jsii_name="addTargets")
    def add_targets(
        self,
        id: builtins.str,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[IApplicationLoadBalancerTarget]] = None,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> "ApplicationTargetGroup":
        '''(experimental) Load balance incoming requests to the given load balancing targets.

        This method implicitly creates an ApplicationTargetGroup for the targets
        involved, and a 'forward' action to route traffic to the given TargetGroup.

        If you want more control over the precise setup, create the TargetGroup
        and use ``addAction`` yourself.

        It's possible to add conditions to the targets added in this way. At least
        one set of targets must be added without conditions.

        :param id: -
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: Duration.minutes(5)
        :param health_check: (experimental) Health check configuration. Default: No health check
        :param port: (experimental) The port on which the listener listens for requests. Default: Determined from protocol if known
        :param protocol: (experimental) The protocol to use. Default: Determined from port if known
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Stickiness disabled
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: Automatically generated
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. All target must be of the same type.
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param priority: (experimental) Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults

        :return: The newly created target group

        :stability: experimental
        '''
        props = AddApplicationTargetsProps(
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            port=port,
            protocol=protocol,
            protocol_version=protocol_version,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            stickiness_cookie_name=stickiness_cookie_name,
            target_group_name=target_group_name,
            targets=targets,
            conditions=conditions,
            priority=priority,
        )

        return typing.cast("ApplicationTargetGroup", jsii.invoke(self, "addTargets", [id, props]))

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: _Port_85922693,
    ) -> None:
        '''(experimental) Register that a connectable that has been added to this load balancer.

        Don't call this directly. It is called by ApplicationTargetGroup.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerConnectable", [connectable, port_range]))

    @jsii.member(jsii_name="validateListener")
    def _validate_listener(self) -> typing.List[builtins.str]:
        '''(experimental) Validate this listener.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateListener", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_0f31fce8:
        '''(experimental) Manage connections to this ApplicationListener.

        :stability: experimental
        '''
        return typing.cast(_Connections_0f31fce8, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> "IApplicationLoadBalancer":
        '''(experimental) Load balancer this listener is associated with.

        :stability: experimental
        '''
        return typing.cast("IApplicationLoadBalancer", jsii.get(self, "loadBalancer"))


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerLookupOptions",
    jsii_struct_bases=[BaseListenerLookupOptions],
    name_mapping={
        "listener_port": "listenerPort",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "listener_arn": "listenerArn",
        "listener_protocol": "listenerProtocol",
    },
)
class ApplicationListenerLookupOptions(BaseListenerLookupOptions):
    def __init__(
        self,
        *,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_protocol: typing.Optional[ApplicationProtocol] = None,
    ) -> None:
        '''(experimental) Options for ApplicationListener lookup.

        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by listener port
        :param load_balancer_arn: (experimental) Filter listeners by associated load balancer arn. Default: - does not filter by load balancer arn
        :param load_balancer_tags: (experimental) Filter listeners by associated load balancer tags. Default: - does not filter by load balancer tags
        :param listener_arn: (experimental) ARN of the listener to look up. Default: - does not filter by listener arn
        :param listener_protocol: (experimental) Filter listeners by listener protocol. Default: - does not filter by listener protocol

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Filter listeners by listener port.

        :default: - does not filter by listener port

        :stability: experimental
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filter listeners by associated load balancer arn.

        :default: - does not filter by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Filter listeners by associated load balancer tags.

        :default: - does not filter by load balancer tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN of the listener to look up.

        :default: - does not filter by listener arn

        :stability: experimental
        '''
        result = self._values.get("listener_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listener_protocol(self) -> typing.Optional[ApplicationProtocol]:
        '''(experimental) Filter listeners by listener protocol.

        :default: - does not filter by listener protocol

        :stability: experimental
        '''
        result = self._values.get("listener_protocol")
        return typing.cast(typing.Optional[ApplicationProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerProps",
    jsii_struct_bases=[BaseApplicationListenerProps],
    name_mapping={
        "certificates": "certificates",
        "default_action": "defaultAction",
        "default_target_groups": "defaultTargetGroups",
        "open": "open",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
        "load_balancer": "loadBalancer",
    },
)
class ApplicationListenerProps(BaseApplicationListenerProps):
    def __init__(
        self,
        *,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
        load_balancer: "IApplicationLoadBalancer",
    ) -> None:
        '''(experimental) Properties for defining a standalone ApplicationListener.

        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.
        :param load_balancer: (experimental) The load balancer to attach this listener to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "load_balancer": load_balancer,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if default_target_groups is not None:
            self._values["default_target_groups"] = default_target_groups
        if open is not None:
            self._values["open"] = open
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[IListenerCertificate]]:
        '''(experimental) Certificate list of ACM cert ARNs.

        :default: - No certificates.

        :stability: experimental
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[IListenerCertificate]], result)

    @builtins.property
    def default_action(self) -> typing.Optional[ListenerAction]:
        '''(experimental) Default action to take for requests to this listener.

        This allows full control of the default action of the load balancer,
        including Action chaining, fixed responses and redirect responses.

        See the ``ListenerAction`` class for all options.

        Cannot be specified together with ``defaultTargetGroups``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[ListenerAction], result)

    @builtins.property
    def default_target_groups(
        self,
    ) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        '''(experimental) Default target groups to load balance to.

        All target groups will be load balanced to with equal weight and without
        stickiness. For a more complex configuration than that, use
        either ``defaultAction`` or ``addAction()``.

        Cannot be specified together with ``defaultAction``.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("default_target_groups")
        return typing.cast(typing.Optional[typing.List["IApplicationTargetGroup"]], result)

    @builtins.property
    def open(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow anyone to connect to this listener.

        If this is specified, the listener will be opened up to anyone who can reach it.
        For internal load balancers this is anyone in the same VPC. For public load
        balancers, this is anyone on the internet.

        If you want to be more selective about who can access this load
        balancer, set this to ``false`` and use the listener's ``connections``
        object to selectively grant access to the listener.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("open")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port on which the listener listens for requests.

        :default: - Determined from protocol if known.

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        '''(experimental) The protocol to use.

        :default: - Determined from port if known.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ApplicationProtocol], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[SslPolicy]:
        '''(experimental) The security policy that defines which ciphers and protocols are supported.

        :default: - The current predefined security policy.

        :stability: experimental
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[SslPolicy], result)

    @builtins.property
    def load_balancer(self) -> "IApplicationLoadBalancer":
        '''(experimental) The load balancer to attach this listener to.

        :stability: experimental
        '''
        result = self._values.get("load_balancer")
        assert result is not None, "Required property 'load_balancer' is missing"
        return typing.cast("IApplicationLoadBalancer", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationListenerRuleProps",
    jsii_struct_bases=[BaseApplicationListenerRuleProps],
    name_mapping={
        "priority": "priority",
        "action": "action",
        "conditions": "conditions",
        "target_groups": "targetGroups",
        "listener": "listener",
    },
)
class ApplicationListenerRuleProps(BaseApplicationListenerRuleProps):
    def __init__(
        self,
        *,
        priority: jsii.Number,
        action: typing.Optional[ListenerAction] = None,
        conditions: typing.Optional[typing.Sequence[ListenerCondition]] = None,
        target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        listener: IApplicationListener,
    ) -> None:
        '''(experimental) Properties for defining a listener rule.

        :param priority: (experimental) Priority of the rule. The rule with the lowest priority will be used for every request. Priorities must be unique.
        :param action: (experimental) Action to perform when requests are received. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Default: - No action
        :param conditions: (experimental) Rule applies if matches the conditions. Default: - No conditions.
        :param target_groups: (experimental) Target groups to forward requests to. Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified. Implies a ``forward`` action. Default: - No target groups.
        :param listener: (experimental) The listener to attach the rule to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "priority": priority,
            "listener": listener,
        }
        if action is not None:
            self._values["action"] = action
        if conditions is not None:
            self._values["conditions"] = conditions
        if target_groups is not None:
            self._values["target_groups"] = target_groups

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) Priority of the rule.

        The rule with the lowest priority will be used for every request.

        Priorities must be unique.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def action(self) -> typing.Optional[ListenerAction]:
        '''(experimental) Action to perform when requests are received.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        :default: - No action

        :stability: experimental
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[ListenerAction], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[ListenerCondition]]:
        '''(experimental) Rule applies if matches the conditions.

        :default: - No conditions.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html
        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[ListenerCondition]], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["IApplicationTargetGroup"]]:
        '''(experimental) Target groups to forward requests to.

        Only one of ``action``, ``fixedResponse``, ``redirectResponse`` or ``targetGroups`` can be specified.

        Implies a ``forward`` action.

        :default: - No target groups.

        :stability: experimental
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List["IApplicationTargetGroup"]], result)

    @builtins.property
    def listener(self) -> IApplicationListener:
        '''(experimental) The listener to attach the rule to.

        :stability: experimental
        '''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast(IApplicationListener, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancerLookupOptions",
    jsii_struct_bases=[BaseLoadBalancerLookupOptions],
    name_mapping={
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class ApplicationLoadBalancerLookupOptions(BaseLoadBalancerLookupOptions):
    def __init__(
        self,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for looking up an ApplicationLoadBalancer.

        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerLookupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancerProps",
    jsii_struct_bases=[BaseLoadBalancerProps],
    name_mapping={
        "vpc": "vpc",
        "deletion_protection": "deletionProtection",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "vpc_subnets": "vpcSubnets",
        "http2_enabled": "http2Enabled",
        "idle_timeout": "idleTimeout",
        "ip_address_type": "ipAddressType",
        "security_group": "securityGroup",
    },
)
class ApplicationLoadBalancerProps(BaseLoadBalancerProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_f30d5663,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_e57d76df] = None,
        http2_enabled: typing.Optional[builtins.bool] = None,
        idle_timeout: typing.Optional[_Duration_4839e8c3] = None,
        ip_address_type: typing.Optional[IpAddressType] = None,
        security_group: typing.Optional[_ISecurityGroup_acf8a799] = None,
    ) -> None:
        '''(experimental) Properties for defining an Application Load Balancer.

        :param vpc: (experimental) The VPC network to place the load balancer in.
        :param deletion_protection: (experimental) Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: (experimental) Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: (experimental) Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: (experimental) Which subnets place the load balancer in. Default: - the Vpc default strategy.
        :param http2_enabled: (experimental) Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: (experimental) The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: (experimental) The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: (experimental) Security group to associate with this load balancer. Default: A security group is created

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_e57d76df(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if http2_enabled is not None:
            self._values["http2_enabled"] = http2_enabled
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def vpc(self) -> _IVpc_f30d5663:
        '''(experimental) The VPC network to place the load balancer in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_f30d5663, result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether deletion protection is enabled.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the load balancer has an internet-routable address.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the load balancer.

        :default: - Automatically generated name.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_e57d76df]:
        '''(experimental) Which subnets place the load balancer in.

        :default: - the Vpc default strategy.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_e57d76df], result)

    @builtins.property
    def http2_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether HTTP/2 is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("http2_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The load balancer idle timeout, in seconds.

        :default: 60

        :stability: experimental
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        '''(experimental) The type of IP addresses to use.

        Only applies to application load balancers.

        :default: IpAddressType.Ipv4

        :stability: experimental
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[IpAddressType], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_acf8a799]:
        '''(experimental) Security group to associate with this load balancer.

        :default: A security group is created

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_acf8a799], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationTargetGroupProps",
    jsii_struct_bases=[BaseTargetGroupProps],
    name_mapping={
        "deregistration_delay": "deregistrationDelay",
        "health_check": "healthCheck",
        "target_group_name": "targetGroupName",
        "target_type": "targetType",
        "vpc": "vpc",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "stickiness_cookie_name": "stickinessCookieName",
        "targets": "targets",
    },
)
class ApplicationTargetGroupProps(BaseTargetGroupProps):
    def __init__(
        self,
        *,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[IApplicationLoadBalancerTarget]] = None,
    ) -> None:
        '''(experimental) Properties for defining an Application Target Group.

        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: (experimental) Health check configuration. Default: - None.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: (experimental) The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: (experimental) The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.

        :stability: experimental
        '''
        if isinstance(health_check, dict):
            health_check = HealthCheck(**health_check)
        self._values: typing.Dict[str, typing.Any] = {}
        if deregistration_delay is not None:
            self._values["deregistration_delay"] = deregistration_delay
        if health_check is not None:
            self._values["health_check"] = health_check
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name
        if target_type is not None:
            self._values["target_type"] = target_type
        if vpc is not None:
            self._values["vpc"] = vpc
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if stickiness_cookie_name is not None:
            self._values["stickiness_cookie_name"] = stickiness_cookie_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def deregistration_delay(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target.

        The range is 0-3600 seconds.

        :default: 300

        :stability: experimental
        '''
        result = self._values.get("deregistration_delay")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheck]:
        '''(experimental) Health check configuration.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheck], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the target group.

        This name must be unique per region per account, can have a maximum of
        32 characters, must contain only alphanumeric characters or hyphens, and
        must not begin or end with a hyphen.

        :default: - Automatically generated.

        :stability: experimental
        '''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional[TargetType]:
        '''(experimental) The type of targets registered to this TargetGroup, either IP or Instance.

        All targets registered into the group must be of this type. If you
        register targets to the TargetGroup in the CDK app, the TargetType is
        determined automatically.

        :default: - Determined automatically.

        :stability: experimental
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[TargetType], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The virtual private cloud (VPC).

        only if ``TargetType`` is ``Ip`` or ``InstanceId``

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_f30d5663], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port on which the listener listens for requests.

        :default: - Determined from protocol if known, optional for Lambda targets.

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ApplicationProtocol]:
        '''(experimental) The protocol to use.

        :default: - Determined from port if known, optional for Lambda targets.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ApplicationProtocol], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[ApplicationProtocolVersion]:
        '''(experimental) The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1

        :stability: experimental
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[ApplicationProtocolVersion], result)

    @builtins.property
    def slow_start(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group.

        The range is 30-900 seconds (15 minutes).

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("slow_start")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_Duration_4839e8c3]:
        '''(experimental) The stickiness cookie expiration period.

        Setting this value enables load balancer stickiness.

        After this period, the cookie is considered stale. The minimum value is
        1 second and the maximum value is 7 days (604800 seconds).

        :default: Duration.days(1)

        :stability: experimental
        '''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_Duration_4839e8c3], result)

    @builtins.property
    def stickiness_cookie_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of an application-based stickiness cookie.

        Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP,
        and AWSALBTG; they're reserved for use by the load balancer.

        Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter.
        If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted.

        :default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html
        :stability: experimental
        '''
        result = self._values.get("stickiness_cookie_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[IApplicationLoadBalancerTarget]]:
        '''(experimental) The targets to add to this target group.

        Can be ``Instance``, ``IPAddress``, or any self-registering load balancing
        target. If you use either ``Instance`` or ``IPAddress`` as targets, all
        target must be of the same type.

        :default: - No targets.

        :stability: experimental
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[IApplicationLoadBalancerTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationLoadBalancer"
)
class IApplicationLoadBalancer(
    ILoadBalancerV2,
    _IConnectable_10015a05,
    typing_extensions.Protocol,
):
    '''(experimental) An application load balancer.

    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) The ARN of this load balancer.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        '''(experimental) The IP Address Type for this load balancer.

        :default: IpAddressType.IPV4

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC this load balancer has been created in (if available).

        If this interface is the result of an import call to fromApplicationLoadBalancerAttributes,
        the vpc attribute will be undefined unless specified in the optional properties of that method.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        '''(experimental) Add a new listener to this load balancer.

        :param id: -
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.

        :stability: experimental
        '''
        ...


class _IApplicationLoadBalancerProxy(
    jsii.proxy_for(ILoadBalancerV2), # type: ignore[misc]
    jsii.proxy_for(_IConnectable_10015a05), # type: ignore[misc]
):
    '''(experimental) An application load balancer.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationLoadBalancer"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerArn")
    def load_balancer_arn(self) -> builtins.str:
        '''(experimental) The ARN of this load balancer.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        '''(experimental) The IP Address Type for this load balancer.

        :default: IpAddressType.IPV4

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IpAddressType], jsii.get(self, "ipAddressType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_IVpc_f30d5663]:
        '''(experimental) The VPC this load balancer has been created in (if available).

        If this interface is the result of an import call to fromApplicationLoadBalancerAttributes,
        the vpc attribute will be undefined unless specified in the optional properties of that method.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IVpc_f30d5663], jsii.get(self, "vpc"))

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence["IApplicationTargetGroup"]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        '''(experimental) Add a new listener to this load balancer.

        :param id: -
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.

        :stability: experimental
        '''
        props = BaseApplicationListenerProps(
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return typing.cast(ApplicationListener, jsii.invoke(self, "addListener", [id, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplicationLoadBalancer).__jsii_proxy_class__ = lambda : _IApplicationLoadBalancerProxy


@jsii.interface(
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationTargetGroup"
)
class IApplicationTargetGroup(ITargetGroup, typing_extensions.Protocol):
    '''(experimental) A Target Group for Application Load Balancers.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: typing.Optional[_Port_85922693] = None,
    ) -> None:
        '''(experimental) Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -

        :stability: experimental
        '''
        ...


class _IApplicationTargetGroupProxy(
    jsii.proxy_for(ITargetGroup) # type: ignore[misc]
):
    '''(experimental) A Target Group for Application Load Balancers.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.IApplicationTargetGroup"

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addTarget", [*targets]))

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: typing.Optional[_Port_85922693] = None,
    ) -> None:
        '''(experimental) Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerConnectable", [connectable, port_range]))

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerListener", [listener, associating_construct]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplicationTargetGroup).__jsii_proxy_class__ = lambda : _IApplicationTargetGroupProxy


@jsii.interface(jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.INetworkTargetGroup")
class INetworkTargetGroup(ITargetGroup, typing_extensions.Protocol):
    '''(experimental) A network target group.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -

        :stability: experimental
        '''
        ...


class _INetworkTargetGroupProxy(
    jsii.proxy_for(ITargetGroup) # type: ignore[misc]
):
    '''(experimental) A network target group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.aws_elasticloadbalancingv2.INetworkTargetGroup"

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addTarget", [*targets]))

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerListener", [listener]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INetworkTargetGroup).__jsii_proxy_class__ = lambda : _INetworkTargetGroupProxy


@jsii.implements(INetworkTargetGroup)
class NetworkTargetGroup(
    TargetGroupBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.NetworkTargetGroup",
):
    '''(experimental) Define a Network Target Group.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        port: jsii.Number,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        protocol: typing.Optional[Protocol] = None,
        proxy_protocol_v2: typing.Optional[builtins.bool] = None,
        targets: typing.Optional[typing.Sequence[INetworkLoadBalancerTarget]] = None,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param port: (experimental) The port on which the listener listens for requests.
        :param preserve_client_ip: (experimental) Indicates whether client IP preservation is enabled. Default: false if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, true.
        :param protocol: (experimental) Protocol for target group, expects TCP, TLS, UDP, or TCP_UDP. Default: - TCP
        :param proxy_protocol_v2: (experimental) Indicates whether Proxy Protocol version 2 is enabled. Default: false
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: (experimental) Health check configuration. Default: - None.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: (experimental) The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: (experimental) The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined

        :stability: experimental
        '''
        props = NetworkTargetGroupProps(
            port=port,
            preserve_client_ip=preserve_client_ip,
            protocol=protocol,
            proxy_protocol_v2=proxy_protocol_v2,
            targets=targets,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            target_group_name=target_group_name,
            target_type=target_type,
            vpc=vpc,
        )

        jsii.create(NetworkTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_target_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> INetworkTargetGroup:
        '''(experimental) Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: (experimental) ARN of the target group.
        :param load_balancer_arns: (experimental) A Token representing the list of ARNs for the load balancer routing to this target group.

        :stability: experimental
        '''
        attrs = TargetGroupAttributes(
            target_group_arn=target_group_arn, load_balancer_arns=load_balancer_arns
        )

        return typing.cast(INetworkTargetGroup, jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: INetworkLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addTarget", [*targets]))

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of targets that are considered healthy.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHealthyHostCount", [props]))

    @jsii.member(jsii_name="metricUnHealthyHostCount")
    def metric_un_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of targets that are considered unhealthy.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricUnHealthyHostCount", [props]))

    @jsii.member(jsii_name="registerListener")
    def register_listener(self, listener: INetworkListener) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerListener", [listener]))

    @jsii.member(jsii_name="validateTargetGroup")
    def _validate_target_group(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateTargetGroup", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        '''(experimental) Full name of first load balancer.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firstLoadBalancerFullName"))


@jsii.implements(IApplicationLoadBalancer)
class ApplicationLoadBalancer(
    BaseLoadBalancer,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationLoadBalancer",
):
    '''(experimental) Define an Application Load Balancer.

    :stability: experimental
    :resource: AWS::ElasticLoadBalancingV2::LoadBalancer
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        http2_enabled: typing.Optional[builtins.bool] = None,
        idle_timeout: typing.Optional[_Duration_4839e8c3] = None,
        ip_address_type: typing.Optional[IpAddressType] = None,
        security_group: typing.Optional[_ISecurityGroup_acf8a799] = None,
        vpc: _IVpc_f30d5663,
        deletion_protection: typing.Optional[builtins.bool] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_e57d76df] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param http2_enabled: (experimental) Indicates whether HTTP/2 is enabled. Default: true
        :param idle_timeout: (experimental) The load balancer idle timeout, in seconds. Default: 60
        :param ip_address_type: (experimental) The type of IP addresses to use. Only applies to application load balancers. Default: IpAddressType.Ipv4
        :param security_group: (experimental) Security group to associate with this load balancer. Default: A security group is created
        :param vpc: (experimental) The VPC network to place the load balancer in.
        :param deletion_protection: (experimental) Indicates whether deletion protection is enabled. Default: false
        :param internet_facing: (experimental) Whether the load balancer has an internet-routable address. Default: false
        :param load_balancer_name: (experimental) Name of the load balancer. Default: - Automatically generated name.
        :param vpc_subnets: (experimental) Which subnets place the load balancer in. Default: - the Vpc default strategy.

        :stability: experimental
        '''
        props = ApplicationLoadBalancerProps(
            http2_enabled=http2_enabled,
            idle_timeout=idle_timeout,
            ip_address_type=ip_address_type,
            security_group=security_group,
            vpc=vpc,
            deletion_protection=deletion_protection,
            internet_facing=internet_facing,
            load_balancer_name=load_balancer_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(ApplicationLoadBalancer, self, [scope, id, props])

    @jsii.member(jsii_name="fromApplicationLoadBalancerAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_application_load_balancer_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: builtins.str,
        security_group_id: builtins.str,
        load_balancer_canonical_hosted_zone_id: typing.Optional[builtins.str] = None,
        load_balancer_dns_name: typing.Optional[builtins.str] = None,
        security_group_allows_all_outbound: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> IApplicationLoadBalancer:
        '''(experimental) Import an existing Application Load Balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: (experimental) ARN of the load balancer.
        :param security_group_id: (experimental) ID of the load balancer's security group.
        :param load_balancer_canonical_hosted_zone_id: (experimental) The canonical hosted zone ID of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param load_balancer_dns_name: (experimental) The DNS name of this load balancer. Default: - When not provided, LB cannot be used as Route53 Alias target.
        :param security_group_allows_all_outbound: (experimental) Whether the security group allows all outbound traffic or not. Unless set to ``false``, no egress rules will be added to the security group. Default: true
        :param vpc: (experimental) The VPC this load balancer has been created in, if available. Default: - If the Load Balancer was imported and a VPC was not specified, the VPC is not available.

        :stability: experimental
        '''
        attrs = ApplicationLoadBalancerAttributes(
            load_balancer_arn=load_balancer_arn,
            security_group_id=security_group_id,
            load_balancer_canonical_hosted_zone_id=load_balancer_canonical_hosted_zone_id,
            load_balancer_dns_name=load_balancer_dns_name,
            security_group_allows_all_outbound=security_group_allows_all_outbound,
            vpc=vpc,
        )

        return typing.cast(IApplicationLoadBalancer, jsii.sinvoke(cls, "fromApplicationLoadBalancerAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromLookup") # type: ignore[misc]
    @builtins.classmethod
    def from_lookup(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> IApplicationLoadBalancer:
        '''(experimental) Look up an application load balancer.

        :param scope: -
        :param id: -
        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        '''
        options = ApplicationLoadBalancerLookupOptions(
            load_balancer_arn=load_balancer_arn, load_balancer_tags=load_balancer_tags
        )

        return typing.cast(IApplicationLoadBalancer, jsii.sinvoke(cls, "fromLookup", [scope, id, options]))

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        certificates: typing.Optional[typing.Sequence[IListenerCertificate]] = None,
        default_action: typing.Optional[ListenerAction] = None,
        default_target_groups: typing.Optional[typing.Sequence[IApplicationTargetGroup]] = None,
        open: typing.Optional[builtins.bool] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        ssl_policy: typing.Optional[SslPolicy] = None,
    ) -> ApplicationListener:
        '''(experimental) Add a new listener to this load balancer.

        :param id: -
        :param certificates: (experimental) Certificate list of ACM cert ARNs. Default: - No certificates.
        :param default_action: (experimental) Default action to take for requests to this listener. This allows full control of the default action of the load balancer, including Action chaining, fixed responses and redirect responses. See the ``ListenerAction`` class for all options. Cannot be specified together with ``defaultTargetGroups``. Default: - None.
        :param default_target_groups: (experimental) Default target groups to load balance to. All target groups will be load balanced to with equal weight and without stickiness. For a more complex configuration than that, use either ``defaultAction`` or ``addAction()``. Cannot be specified together with ``defaultAction``. Default: - None.
        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known.
        :param ssl_policy: (experimental) The security policy that defines which ciphers and protocols are supported. Default: - The current predefined security policy.

        :stability: experimental
        '''
        props = BaseApplicationListenerProps(
            certificates=certificates,
            default_action=default_action,
            default_target_groups=default_target_groups,
            open=open,
            port=port,
            protocol=protocol,
            ssl_policy=ssl_policy,
        )

        return typing.cast(ApplicationListener, jsii.invoke(self, "addListener", [id, props]))

    @jsii.member(jsii_name="addRedirect")
    def add_redirect(
        self,
        *,
        open: typing.Optional[builtins.bool] = None,
        source_port: typing.Optional[jsii.Number] = None,
        source_protocol: typing.Optional[ApplicationProtocol] = None,
        target_port: typing.Optional[jsii.Number] = None,
        target_protocol: typing.Optional[ApplicationProtocol] = None,
    ) -> ApplicationListener:
        '''(experimental) Add a redirection listener to this load balancer.

        :param open: (experimental) Allow anyone to connect to this listener. If this is specified, the listener will be opened up to anyone who can reach it. For internal load balancers this is anyone in the same VPC. For public load balancers, this is anyone on the internet. If you want to be more selective about who can access this load balancer, set this to ``false`` and use the listener's ``connections`` object to selectively grant access to the listener. Default: true
        :param source_port: (experimental) The port number to listen to. Default: 80
        :param source_protocol: (experimental) The protocol of the listener being created. Default: HTTP
        :param target_port: (experimental) The port number to redirect to. Default: 443
        :param target_protocol: (experimental) The protocol of the redirection target. Default: HTTPS

        :stability: experimental
        '''
        props = ApplicationLoadBalancerRedirectConfig(
            open=open,
            source_port=source_port,
            source_protocol=source_protocol,
            target_port=target_port,
            target_protocol=target_protocol,
        )

        return typing.cast(ApplicationListener, jsii.invoke(self, "addRedirect", [props]))

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, security_group: _ISecurityGroup_acf8a799) -> None:
        '''(experimental) Add a security group to this load balancer.

        :param security_group: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addSecurityGroup", [security_group]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) Return the given named metric for this Application Load Balancer.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricActiveConnectionCount")
    def metric_active_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of concurrent TCP connections active from clients to the load balancer and from the load balancer to targets.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricActiveConnectionCount", [props]))

    @jsii.member(jsii_name="metricClientTlsNegotiationErrorCount")
    def metric_client_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of TLS connections initiated by the client that did not establish a session with the load balancer.

        Possible causes include a
        mismatch of ciphers or protocols.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricClientTlsNegotiationErrorCount", [props]))

    @jsii.member(jsii_name="metricConsumedLCUs")
    def metric_consumed_lc_us(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of load balancer capacity units (LCU) used by your load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricConsumedLCUs", [props]))

    @jsii.member(jsii_name="metricElbAuthError")
    def metric_elb_auth_error(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of user authentications that could not be completed.

        Because an authenticate action was misconfigured, the load balancer
        couldn't establish a connection with the IdP, or the load balancer
        couldn't complete the authentication flow due to an internal error.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricElbAuthError", [props]))

    @jsii.member(jsii_name="metricElbAuthFailure")
    def metric_elb_auth_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of user authentications that could not be completed because the IdP denied access to the user or an authorization code was used more than once.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricElbAuthFailure", [props]))

    @jsii.member(jsii_name="metricElbAuthLatency")
    def metric_elb_auth_latency(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The time elapsed, in milliseconds, to query the IdP for the ID token and user info.

        If one or more of these operations fail, this is the time to failure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricElbAuthLatency", [props]))

    @jsii.member(jsii_name="metricElbAuthSuccess")
    def metric_elb_auth_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of authenticate actions that were successful.

        This metric is incremented at the end of the authentication workflow,
        after the load balancer has retrieved the user claims from the IdP.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricElbAuthSuccess", [props]))

    @jsii.member(jsii_name="metricHttpCodeElb")
    def metric_http_code_elb(
        self,
        code: HttpCodeElb,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of HTTP 3xx/4xx/5xx codes that originate from the load balancer.

        This does not include any response codes generated by the targets.

        :param code: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpCodeElb", [code, props]))

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(
        self,
        code: HttpCodeTarget,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in the load balancer.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpCodeTarget", [code, props]))

    @jsii.member(jsii_name="metricHttpFixedResponseCount")
    def metric_http_fixed_response_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of fixed-response actions that were successful.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpFixedResponseCount", [props]))

    @jsii.member(jsii_name="metricHttpRedirectCount")
    def metric_http_redirect_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of redirect actions that were successful.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpRedirectCount", [props]))

    @jsii.member(jsii_name="metricHttpRedirectUrlLimitExceededCount")
    def metric_http_redirect_url_limit_exceeded_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of redirect actions that couldn't be completed because the URL in the response location header is larger than 8K.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpRedirectUrlLimitExceededCount", [props]))

    @jsii.member(jsii_name="metricIpv6ProcessedBytes")
    def metric_ipv6_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of bytes processed by the load balancer over IPv6.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricIpv6ProcessedBytes", [props]))

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of IPv6 requests received by the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricIpv6RequestCount", [props]))

    @jsii.member(jsii_name="metricNewConnectionCount")
    def metric_new_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of new TCP connections established from clients to the load balancer and from the load balancer to targets.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricNewConnectionCount", [props]))

    @jsii.member(jsii_name="metricProcessedBytes")
    def metric_processed_bytes(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The total number of bytes processed by the load balancer over IPv4 and IPv6.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricProcessedBytes", [props]))

    @jsii.member(jsii_name="metricRejectedConnectionCount")
    def metric_rejected_connection_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of connections that were rejected because the load balancer had reached its maximum number of connections.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricRejectedConnectionCount", [props]))

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricRequestCount", [props]))

    @jsii.member(jsii_name="metricRuleEvaluations")
    def metric_rule_evaluations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of rules processed by the load balancer given a request rate averaged over an hour.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricRuleEvaluations", [props]))

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of connections that were not successfully established between the load balancer and target.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetConnectionErrorCount", [props]))

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetResponseTime", [props]))

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_0f31fce8:
        '''
        :stability: experimental
        '''
        return typing.cast(_Connections_0f31fce8, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[IpAddressType]:
        '''(experimental) The IP Address Type for this load balancer.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IpAddressType], jsii.get(self, "ipAddressType"))


@jsii.implements(IApplicationTargetGroup)
class ApplicationTargetGroup(
    TargetGroupBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_elasticloadbalancingv2.ApplicationTargetGroup",
):
    '''(experimental) Define an Application Target Group.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[ApplicationProtocol] = None,
        protocol_version: typing.Optional[ApplicationProtocolVersion] = None,
        slow_start: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_duration: typing.Optional[_Duration_4839e8c3] = None,
        stickiness_cookie_name: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Sequence[IApplicationLoadBalancerTarget]] = None,
        deregistration_delay: typing.Optional[_Duration_4839e8c3] = None,
        health_check: typing.Optional[HealthCheck] = None,
        target_group_name: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[TargetType] = None,
        vpc: typing.Optional[_IVpc_f30d5663] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param port: (experimental) The port on which the listener listens for requests. Default: - Determined from protocol if known, optional for Lambda targets.
        :param protocol: (experimental) The protocol to use. Default: - Determined from port if known, optional for Lambda targets.
        :param protocol_version: (experimental) The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param slow_start: (experimental) The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic to the target group. The range is 30-900 seconds (15 minutes). Default: 0
        :param stickiness_cookie_duration: (experimental) The stickiness cookie expiration period. Setting this value enables load balancer stickiness. After this period, the cookie is considered stale. The minimum value is 1 second and the maximum value is 7 days (604800 seconds). Default: Duration.days(1)
        :param stickiness_cookie_name: (experimental) The name of an application-based stickiness cookie. Names that start with the following prefixes are not allowed: AWSALB, AWSALBAPP, and AWSALBTG; they're reserved for use by the load balancer. Note: ``stickinessCookieName`` parameter depends on the presence of ``stickinessCookieDuration`` parameter. If ``stickinessCookieDuration`` is not set, ``stickinessCookieName`` will be omitted. Default: - If ``stickinessCookieDuration`` is set, a load-balancer generated cookie is used. Otherwise, no stickiness is defined.
        :param targets: (experimental) The targets to add to this target group. Can be ``Instance``, ``IPAddress``, or any self-registering load balancing target. If you use either ``Instance`` or ``IPAddress`` as targets, all target must be of the same type. Default: - No targets.
        :param deregistration_delay: (experimental) The amount of time for Elastic Load Balancing to wait before deregistering a target. The range is 0-3600 seconds. Default: 300
        :param health_check: (experimental) Health check configuration. Default: - None.
        :param target_group_name: (experimental) The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. Default: - Automatically generated.
        :param target_type: (experimental) The type of targets registered to this TargetGroup, either IP or Instance. All targets registered into the group must be of this type. If you register targets to the TargetGroup in the CDK app, the TargetType is determined automatically. Default: - Determined automatically.
        :param vpc: (experimental) The virtual private cloud (VPC). only if ``TargetType`` is ``Ip`` or ``InstanceId`` Default: - undefined

        :stability: experimental
        '''
        props = ApplicationTargetGroupProps(
            port=port,
            protocol=protocol,
            protocol_version=protocol_version,
            slow_start=slow_start,
            stickiness_cookie_duration=stickiness_cookie_duration,
            stickiness_cookie_name=stickiness_cookie_name,
            targets=targets,
            deregistration_delay=deregistration_delay,
            health_check=health_check,
            target_group_name=target_group_name,
            target_type=target_type,
            vpc=vpc,
        )

        jsii.create(ApplicationTargetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromTargetGroupAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_target_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_group_arn: builtins.str,
        load_balancer_arns: typing.Optional[builtins.str] = None,
    ) -> IApplicationTargetGroup:
        '''(experimental) Import an existing target group.

        :param scope: -
        :param id: -
        :param target_group_arn: (experimental) ARN of the target group.
        :param load_balancer_arns: (experimental) A Token representing the list of ARNs for the load balancer routing to this target group.

        :stability: experimental
        '''
        attrs = TargetGroupAttributes(
            target_group_arn=target_group_arn, load_balancer_arns=load_balancer_arns
        )

        return typing.cast(IApplicationTargetGroup, jsii.sinvoke(cls, "fromTargetGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, *targets: IApplicationLoadBalancerTarget) -> None:
        '''(experimental) Add a load balancing target to this target group.

        :param targets: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addTarget", [*targets]))

    @jsii.member(jsii_name="enableCookieStickiness")
    def enable_cookie_stickiness(
        self,
        duration: _Duration_4839e8c3,
        cookie_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Enable sticky routing via a cookie to members of this target group.

        Note: If the ``cookieName`` parameter is set, application-based stickiness will be applied,
        otherwise it defaults to duration-based stickiness attributes (``lb_cookie``).

        :param duration: -
        :param cookie_name: -

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html
        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "enableCookieStickiness", [duration, cookie_name]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) Return the given named metric for this Application Load Balancer Target Group.

        Returns the metric for this target group from the point of view of the first
        load balancer load balancing to it. If you have multiple load balancers load
        sending traffic to the same target group, you will have to override the dimensions
        on this metric.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricHealthyHostCount")
    def metric_healthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of healthy hosts in the target group.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHealthyHostCount", [props]))

    @jsii.member(jsii_name="metricHttpCodeTarget")
    def metric_http_code_target(
        self,
        code: HttpCodeTarget,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of HTTP 2xx/3xx/4xx/5xx response codes generated by all targets in this target group.

        This does not include any response codes generated by the load balancer.

        :param code: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricHttpCodeTarget", [code, props]))

    @jsii.member(jsii_name="metricIpv6RequestCount")
    def metric_ipv6_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of IPv6 requests received by the target group.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricIpv6RequestCount", [props]))

    @jsii.member(jsii_name="metricRequestCount")
    def metric_request_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of requests processed over IPv4 and IPv6.

        This count includes only the requests with a response generated by a target of the load balancer.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricRequestCount", [props]))

    @jsii.member(jsii_name="metricRequestCountPerTarget")
    def metric_request_count_per_target(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The average number of requests received by each target in a target group.

        The only valid statistic is Sum. Note that this represents the average not the sum.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricRequestCountPerTarget", [props]))

    @jsii.member(jsii_name="metricTargetConnectionErrorCount")
    def metric_target_connection_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of connections that were not successfully established between the load balancer and target.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetConnectionErrorCount", [props]))

    @jsii.member(jsii_name="metricTargetResponseTime")
    def metric_target_response_time(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The time elapsed, in seconds, after the request leaves the load balancer until a response from the target is received.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetResponseTime", [props]))

    @jsii.member(jsii_name="metricTargetTLSNegotiationErrorCount")
    def metric_target_tls_negotiation_error_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of TLS connections initiated by the load balancer that did not establish a session with the target.

        Possible causes include a mismatch of ciphers or protocols.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Sum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricTargetTLSNegotiationErrorCount", [props]))

    @jsii.member(jsii_name="metricUnhealthyHostCount")
    def metric_unhealthy_host_count(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_4839e8c3] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_61bc6f70] = None,
    ) -> _Metric_e396a4dc:
        '''(experimental) The number of unhealthy hosts in the target group.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: Average over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1788b62f(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_e396a4dc, jsii.invoke(self, "metricUnhealthyHostCount", [props]))

    @jsii.member(jsii_name="registerConnectable")
    def register_connectable(
        self,
        connectable: _IConnectable_10015a05,
        port_range: typing.Optional[_Port_85922693] = None,
    ) -> None:
        '''(experimental) Register a connectable as a member of this target group.

        Don't call this directly. It will be called by load balancing targets.

        :param connectable: -
        :param port_range: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerConnectable", [connectable, port_range]))

    @jsii.member(jsii_name="registerListener")
    def register_listener(
        self,
        listener: IApplicationListener,
        associating_construct: typing.Optional[constructs.IConstruct] = None,
    ) -> None:
        '''(experimental) Register a listener that is load balancing to this target group.

        Don't call this directly. It will be called by listeners.

        :param listener: -
        :param associating_construct: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "registerListener", [listener, associating_construct]))

    @jsii.member(jsii_name="validateTargetGroup")
    def _validate_target_group(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateTargetGroup", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="firstLoadBalancerFullName")
    def first_load_balancer_full_name(self) -> builtins.str:
        '''(experimental) Full name of first load balancer.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firstLoadBalancerFullName"))


__all__ = [
    "AddApplicationActionProps",
    "AddApplicationTargetGroupsProps",
    "AddApplicationTargetsProps",
    "AddNetworkActionProps",
    "AddNetworkTargetsProps",
    "AddRuleProps",
    "ApplicationListener",
    "ApplicationListenerAttributes",
    "ApplicationListenerCertificate",
    "ApplicationListenerCertificateProps",
    "ApplicationListenerLookupOptions",
    "ApplicationListenerProps",
    "ApplicationListenerRule",
    "ApplicationListenerRuleProps",
    "ApplicationLoadBalancer",
    "ApplicationLoadBalancerAttributes",
    "ApplicationLoadBalancerLookupOptions",
    "ApplicationLoadBalancerProps",
    "ApplicationLoadBalancerRedirectConfig",
    "ApplicationProtocol",
    "ApplicationProtocolVersion",
    "ApplicationTargetGroup",
    "ApplicationTargetGroupProps",
    "AuthenticateOidcOptions",
    "BaseApplicationListenerProps",
    "BaseApplicationListenerRuleProps",
    "BaseListener",
    "BaseListenerLookupOptions",
    "BaseLoadBalancer",
    "BaseLoadBalancerLookupOptions",
    "BaseLoadBalancerProps",
    "BaseNetworkListenerProps",
    "BaseTargetGroupProps",
    "CfnListener",
    "CfnListenerCertificate",
    "CfnListenerCertificateProps",
    "CfnListenerProps",
    "CfnListenerRule",
    "CfnListenerRuleProps",
    "CfnLoadBalancer",
    "CfnLoadBalancerProps",
    "CfnTargetGroup",
    "CfnTargetGroupProps",
    "FixedResponseOptions",
    "ForwardOptions",
    "HealthCheck",
    "HttpCodeElb",
    "HttpCodeTarget",
    "IApplicationListener",
    "IApplicationLoadBalancer",
    "IApplicationLoadBalancerTarget",
    "IApplicationTargetGroup",
    "IListenerAction",
    "IListenerCertificate",
    "ILoadBalancerV2",
    "INetworkListener",
    "INetworkLoadBalancer",
    "INetworkLoadBalancerTarget",
    "INetworkTargetGroup",
    "ITargetGroup",
    "IpAddressType",
    "ListenerAction",
    "ListenerCertificate",
    "ListenerCondition",
    "LoadBalancerTargetProps",
    "NetworkForwardOptions",
    "NetworkListener",
    "NetworkListenerAction",
    "NetworkListenerLookupOptions",
    "NetworkListenerProps",
    "NetworkLoadBalancer",
    "NetworkLoadBalancerAttributes",
    "NetworkLoadBalancerLookupOptions",
    "NetworkLoadBalancerProps",
    "NetworkTargetGroup",
    "NetworkTargetGroupProps",
    "NetworkWeightedTargetGroup",
    "Protocol",
    "QueryStringCondition",
    "RedirectOptions",
    "SslPolicy",
    "TargetGroupAttributes",
    "TargetGroupBase",
    "TargetType",
    "UnauthenticatedAction",
    "WeightedTargetGroup",
]

publication.publish()

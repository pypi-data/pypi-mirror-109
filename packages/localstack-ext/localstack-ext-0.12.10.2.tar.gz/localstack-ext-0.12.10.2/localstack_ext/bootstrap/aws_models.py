from localstack.utils.aws import aws_models
gakzn=super
gakzq=None
gakzH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gakzn(LambdaLayer,self).__init__(arn)
  self.cwd=gakzq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.gakzH.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(RDSDatabase,self).__init__(gakzH,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(RDSCluster,self).__init__(gakzH,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(AppSyncAPI,self).__init__(gakzH,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(AmplifyApp,self).__init__(gakzH,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(ElastiCacheCluster,self).__init__(gakzH,env=env)
class TransferServer(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(TransferServer,self).__init__(gakzH,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(CloudFrontDistribution,self).__init__(gakzH,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,gakzH,env=gakzq):
  gakzn(CodeCommitRepository,self).__init__(gakzH,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

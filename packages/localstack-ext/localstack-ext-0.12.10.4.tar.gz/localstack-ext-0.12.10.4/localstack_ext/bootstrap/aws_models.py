from localstack.utils.aws import aws_models
Smxkg=super
Smxkw=None
Smxks=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Smxkg(LambdaLayer,self).__init__(arn)
  self.cwd=Smxkw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Smxks.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(RDSDatabase,self).__init__(Smxks,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(RDSCluster,self).__init__(Smxks,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(AppSyncAPI,self).__init__(Smxks,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(AmplifyApp,self).__init__(Smxks,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(ElastiCacheCluster,self).__init__(Smxks,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(TransferServer,self).__init__(Smxks,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(CloudFrontDistribution,self).__init__(Smxks,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Smxks,env=Smxkw):
  Smxkg(CodeCommitRepository,self).__init__(Smxks,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

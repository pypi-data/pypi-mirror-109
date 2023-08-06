from localstack.utils.aws import aws_models
emXkd=super
emXkJ=None
emXkb=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  emXkd(LambdaLayer,self).__init__(arn)
  self.cwd=emXkJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.emXkb.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(RDSDatabase,self).__init__(emXkb,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(RDSCluster,self).__init__(emXkb,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(AppSyncAPI,self).__init__(emXkb,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(AmplifyApp,self).__init__(emXkb,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(ElastiCacheCluster,self).__init__(emXkb,env=env)
class TransferServer(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(TransferServer,self).__init__(emXkb,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(CloudFrontDistribution,self).__init__(emXkb,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,emXkb,env=emXkJ):
  emXkd(CodeCommitRepository,self).__init__(emXkb,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

from localstack.utils.aws import aws_models
pxMHJ=super
pxMHK=None
pxMHi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pxMHJ(LambdaLayer,self).__init__(arn)
  self.cwd=pxMHK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pxMHi.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(RDSDatabase,self).__init__(pxMHi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(RDSCluster,self).__init__(pxMHi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(AppSyncAPI,self).__init__(pxMHi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(AmplifyApp,self).__init__(pxMHi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(ElastiCacheCluster,self).__init__(pxMHi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(TransferServer,self).__init__(pxMHi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(CloudFrontDistribution,self).__init__(pxMHi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pxMHi,env=pxMHK):
  pxMHJ(CodeCommitRepository,self).__init__(pxMHi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

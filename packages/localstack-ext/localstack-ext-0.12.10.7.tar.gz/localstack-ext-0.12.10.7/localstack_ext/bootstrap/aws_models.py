from localstack.utils.aws import aws_models
lIPsC=super
lIPsn=None
lIPse=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lIPsC(LambdaLayer,self).__init__(arn)
  self.cwd=lIPsn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lIPse.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(RDSDatabase,self).__init__(lIPse,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(RDSCluster,self).__init__(lIPse,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(AppSyncAPI,self).__init__(lIPse,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(AmplifyApp,self).__init__(lIPse,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(ElastiCacheCluster,self).__init__(lIPse,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(TransferServer,self).__init__(lIPse,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(CloudFrontDistribution,self).__init__(lIPse,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lIPse,env=lIPsn):
  lIPsC(CodeCommitRepository,self).__init__(lIPse,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

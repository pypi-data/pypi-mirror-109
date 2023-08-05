from localstack.utils.aws import aws_models
YQriV=super
YQriR=None
YQria=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YQriV(LambdaLayer,self).__init__(arn)
  self.cwd=YQriR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YQria.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(RDSDatabase,self).__init__(YQria,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(RDSCluster,self).__init__(YQria,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(AppSyncAPI,self).__init__(YQria,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(AmplifyApp,self).__init__(YQria,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(ElastiCacheCluster,self).__init__(YQria,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(TransferServer,self).__init__(YQria,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(CloudFrontDistribution,self).__init__(YQria,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YQria,env=YQriR):
  YQriV(CodeCommitRepository,self).__init__(YQria,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

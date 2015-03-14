# coding: utf-8
'''
Created on 2014年10月20日

@author: cuimingwen
'''
from virBase import VirBase

class VirGlanceUtil(VirBase):
    '''
    classdocs
    '''


    def __init__(self, params=None,resource_id=None):
        '''
        Constructor
        '''
        super(VirGlanceUtil,self).__init__(resource_id=resource_id)
        
    def getGlanceImageExists(self,  mkey='image'):
        ' iamge exists or not '
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getGlanceImageSize(self, mkey='image.size'):
        ' already  update image size'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getGlanceImageDelete(self, mkey='image.delete'):
        ' 镜像删除次数'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getGlanceImageUpdate(self, mkey='image.update'):
        ' 镜像更新次数'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getGlanceImageUpload(self, mkey='image.upload'):
        ' 镜像上载次数'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt        
            
    def getGlanceImageDownload(self, mkey='image.download'):
        ' 镜像已下载'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getGlanceImageServe(self, mkey='image.serve'):
        ' 镜像已使用   unit(B)'
        imageRlt = self.getMeterSampleByName(mkey=mkey)
        return imageRlt
    
    def getCommonService(self, mkey=None):
        ' get sample  from  monitor key '
        Rlt = self.getMeterSampleByName(mkey=mkey)
        return Rlt        
    
    def __repr__(self):
        return self.__class__.__name__

if __name__ == '__main__':
    t = VirGlanceUtil(resource_id='f57e4f9f-6524-48d7-bd7b-8677085344d2')
    print t.getCommonService('image.serve')
    print t.getGlanceImageExists()
    print t.getGlanceImageDelete()
    print t.getGlanceImageServe()
    print t.getGlanceImageDownload()
    print t.getGlanceImageSize()
    #print t.getGlanceImageDelete()
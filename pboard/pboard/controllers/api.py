# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from datetime import datetime

import cStringIO as csio
import Image as pil

import tg
from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates as tgp


from pboard.lib.base import BaseController
from pboard.lib   import dbapi as pld
from pboard.model import data as pmd
from pboard import model as pm

__all__ = ['PODPublicApiController', 'PODApiController']

class PODPublicApiController(BaseController):

    @expose()
    def create_account(self, email=u'', password=u'', retyped_password=u'', **kw):
      if email==u'' or password==u'' or retyped_password==u'':
        flash(_('Account creation error: please fill all the fields'), 'error')
        redirect(lurl('/'))
      elif password!=retyped_password:
        flash(_('Account creation error: passwords do not match'), 'error')
        redirect(lurl('/'))
      else:
        loExistingUser = pld.PODStaticController.getUserByEmailAddress(email)
        if loExistingUser!=None:
          flash(_('Account creation error: account already exist: %s') % (email), 'error')
          redirect(lurl('/'))
        
        loNewAccount = pld.PODStaticController.createUser()
        loNewAccount.email_address = email
        loNewAccount.display_name  = email
        loNewAccount.password      = password
        loUserGroup = pld.PODStaticController.getGroup('user')
        loUserGroup.users.append(loNewAccount)
        pm.DBSession.flush()
        flash(_('Account successfully created: %s') % (email), 'info')
        redirect(lurl('/'))


class PODApiController(BaseController):
    """Sample controller-wide authorization"""
    
    allow_only = tgp.in_group('user', msg=l_('You need to login in order to access this ressource'))
    
    @expose()
    def create_event(self, parent_id=None, data_label=u'', data_datetime=None, data_content=u'', data_reminder_datetime=None, add_reminder=False, **kw):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNewNode = loApiController.createNode()
      loNewNode.parent_id     = int(parent_id)
      loNewNode.node_type     = pmd.PBNodeType.Event
      loNewNode.data_label    = data_label
      loNewNode.data_content  = data_content
      loNewNode.data_datetime = datetime.strptime(data_datetime, '%d/%m/%Y %H:%M')
      if add_reminder:
        loNewNode.data_reminder_datetime = data_reminder_datetime

      pm.DBSession.flush()
      redirect(lurl('/document/%i'%(loNewNode.parent_id)))

    @expose()
    def create_contact(self, parent_id=None, data_label=u'', data_content=u'', **kw):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNewNode = loApiController.createNode()
      loNewNode.parent_id     = int(parent_id)
      loNewNode.node_type     = pmd.PBNodeType.Contact
      loNewNode.data_label    = data_label
      loNewNode.data_content  = data_content

      pm.DBSession.flush()
      redirect(lurl('/document/%i'%(loNewNode.parent_id)))

    @expose()
    def create_comment(self, parent_id=None, data_label=u'', data_content=u'', **kw):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNewNode = loApiController.createNode()
      loNewNode.parent_id     = int(parent_id)
      loNewNode.node_type     = pmd.PBNodeType.Comment
      loNewNode.data_label    = data_label
      loNewNode.data_content  = data_content

      pm.DBSession.flush()
      redirect(lurl('/document/%i'%(loNewNode.parent_id)))

    @expose()
    def create_file(self, parent_id=None, data_label=u'', data_content=u'', data_file=None, **kw):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNewNode = loApiController.createNode()
      loNewNode.parent_id     = int(parent_id)
      loNewNode.node_type     = pmd.PBNodeType.File
      loNewNode.data_label    = data_label
      loNewNode.data_content  = data_content

      loNewNode.data_file_name      = data_file.filename
      loNewNode.data_file_mime_type = data_file.type
      loNewNode.data_file_content   = data_file.file.read()

      pm.DBSession.flush()
      redirect(lurl('/document/%i'%(loNewNode.parent_id)))

    @expose()
    def get_file_content(self, node_id=None, **kw):
      if node_id==None:
        return
      else:
        loCurrentUser   = pld.PODStaticController.getCurrentUser()
        loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
        loFile = loApiController.getNode(node_id)

        lsContentType = "application/x-download"
        if loFile.data_file_mime_type!='':
          tg.response.headers['Content-type'] = str(loFile.data_file_mime_type)

        tg.response.headers['Content-Type']        = lsContentType
        tg.response.headers['Content-Disposition'] = str('attachment; filename="%s"'%(loFile.data_file_name))
        return loFile.data_file_content

    @expose()
    def get_file_content_thumbnail(self, node_id=None, **kw):
      if node_id==None:
        return
      else:
        loCurrentUser   = pld.PODStaticController.getCurrentUser()
        loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
        
        loFile = loApiController.getNode(node_id)
        
        loJpegBytes = csio.StringIO(loFile.data_file_content)
        loImage     = pil.open(loJpegBytes)
        loImage.thumbnail([140,140], pil.ANTIALIAS)
        
        loResultBuffer = StringIO()
        loImage.save(loResultBuffer,"JPEG")
        tg.response.headers['Content-type'] = str(loFile.data_file_mime_type)
        return loResultBuffer.getvalue()

    @expose()
    def set_parent_node(self, node_id, new_parent_id, **kw):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      # TODO - D.A. - 2013-11-07 - Check that new parent is accessible by the user !!!
      loNewNode = loApiController.getNode(node_id)
      if new_parent_id!='':
        loNewNode.parent_id = int(new_parent_id)
      pm.DBSession.flush()
      redirect(lurl('/document/%s'%(node_id)))

    @expose()
    def move_node_upper(self, node_id=0):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNode = loApiController.getNode(node_id)
      loApiController.moveNodeUpper(loNode)
      redirect(lurl('/document/%s'%(node_id)))

    @expose()
    def move_node_lower(self, node_id=0):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNode = loApiController.getNode(node_id)
      loApiController.moveNodeLower(loNode)
      redirect(lurl('/document/%s'%(node_id)))

    @expose()
    def create_document(self, parent_id=None):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNewNode = loApiController.createDummyNode()
      loNewNode.data_label   = 'New document'
      loNewNode.data_content = 'insert content...'
      if int(parent_id)==0:
        loNewNode.parent_id = None
      else:
        loNewNode.parent_id = parent_id

      pm.DBSession.flush()
      redirect(lurl('/document/%i'%(loNewNode.node_id)))

    @expose()
    def edit_status(self, node_id, node_status):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNode = loApiController.getNode(node_id)
      loNode.node_status = node_status
      redirect(lurl('/document/%s'%(node_id)))

    @expose()
    def edit_label_and_content(self, node_id, data_label, data_content):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      
      loNode = loApiController.getNode(node_id)
      loNode.data_label   = data_label
      loNode.data_content = data_content
      redirect(lurl('/document/%s'%(node_id)))

    @expose()
    def force_delete_node(self, node_id=None):
      loCurrentUser   = pld.PODStaticController.getCurrentUser()
      loApiController = pld.PODUserFilteredApiController(loCurrentUser.user_id)
      loNode = loApiController.getNode(node_id)
      liParentId = loNode.parent_id
      if loNode.getChildNb()<=0:
        pm.DBSession.delete(loNode)
      redirect(lurl('/document/%i'%(liParentId or 0)))

    @expose()
    def reindex_nodes(self, back_to_node_id=0):
      # FIXME - NOT SAFE
      loRootNodeList   = pm.DBSession.query(pmd.PBNode).order_by(pmd.PBNode.parent_id).all()
      for loNode in loRootNodeList:
        if loNode.parent_id==None:
          loNode.node_depth = 0
          loNode.parent_tree_path = '/'
        else:
          loNode.node_depth = loNode._oParent.node_depth+1
          loNode.parent_tree_path = '%s%i/'%(loNode._oParent.parent_tree_path,loNode.parent_id)
      
      pm.DBSession.flush()
      flash(_('Documents re-indexed'), 'info')
      redirect(lurl('/document/%s'%(back_to_node_id)))

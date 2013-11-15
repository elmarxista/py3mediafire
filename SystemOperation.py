 # -*- coding: utf-8 -*-
# -*- Mode: Python; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- #
import hashlib
import os
import mimetypes
import urllib.parse
import urllib.request
import io
import itertools
import mimetypes
import json
import email.generator
from py3mediafire.WapperUrl import WapperUrl
from py3mediafire.BaseUrlMediaFire import BaseUrlMediaFire

class SystemOperation(WapperUrl):
	def __init__(self,ref_session):
		self.__session_token = ref_session
		#folder key mq10rijd8mora
		#self.cut_file('ovlaabbb6pth3ja')
		#print(self.search('focus.rar')[0])
#		for a in range(len(reps)):
#			#print(reps[a])
#			print('--------------------------------------------------------')
#'ovlaabbb6pth3ja'
		original = self.search('torituga')[0]['folderkey']
		#print(self.upload('leonel.jpg'))

	def get_content(self):
		""" Return either a list of folders or a list of files."""
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_CONTENT_FOLDER,
			{'session_token': self.__session_token.get_token(),
			'version': self.__session_token.get_version_actual()})
		return js

	def ls_in_root(self,filter_result = ''):
		"""
		Option for filter_result:
			files,folders,private,public,image,video,document,audio,spreadsheet,
			presentation,application,archive,data,development
		"""
		js = self.get_json_mediafire(BaseUrlMediaFire.SEARCH_FOLDER ,
		{'session_token': self.__session_token.get_token(),
			'filter' : filter_result,
			'search_text' : ' ',
			'search_all' : 'no',
			'version': self.__session_token.get_version_actual()})
		return js['results']

	def ls_in_folder(self,folder_key,filter_result = ''):
		"""
		Option for filter_result:
			files,folders,private,public,image,video,document,audio,spreadsheet,
			presentation,application,archive,data,development
		"""
		js = self.get_json_mediafire(BaseUrlMediaFire.SEARCH_FOLDER ,
		{'folder_key': folder_key,
			'filter' : filter_result,
			'search_text' : ' ',
			'search_all' : 'no',
			'version': self.__session_token.get_version_actual()})
		return js['results']

	def search(self, search_text, option = {}, folder_key = None):
		"""Searches the content of the given folder. If the folder_key is not passed,
		the search will be performed on the root folder (myfiles) and the session token
		will be required. To search the root folder on other devices other than the cloud,
		pass the device_id. If the device_id is -1, then a global search on all devices will
		be performed

		Keyword arguments:
			search_text -- the keywords to search for in filenames, folder names, descriptions and tags(defaul True)
			option -- {} (defaul {})
				filter : filter by privacy and/or by filetype. This is a comma-separated list
					of file types and privacy option. Can take one or more of the following
					values : "public", "private", "image", "video","audio", "document",
					"spreadsheet","presentation", "application", "archive", "data",
						folders,files, and "development"
				device_id :  Specify which device to return the myfiles data from. If not set,
					it defaults to the cloud. if it's set to -1, then search will be performed
					on all devices.
				search_all : 'yes' or 'no'. If folder_key is passed, then this parameter is
					ignored. If folder_key is not passed, search_all can be used to indicate
					whether to search the root folder only or the entire device (default 'yes').
			folder_key -- The key that identifies the folder. If the folder_key is not passed,
				the session token is required and 'search' API will return the root folder
				content. If the folder_key is passed and search_all is set to 'yes,'
				the entire device will be searched. 

		Return json results
		"""
		option['search_text'] = search_text
		option['version'] = self.__session_token.get_version_actual()
		if(folder_key == None):
			option['session_token'] = self.__session_token.get_token()
		else:
			option['folder_key'] = folder_key
		js = self.get_json_mediafire(BaseUrlMediaFire.SEARCH_FOLDER ,option)
		return js['results']

	def perfect_search(self, search_text, option = {}, folder_key = None):
		result = self.search(search_text, option, folder_key)
		if(folder_key == None):
			folder_key = ''
		if(len(result) == 1):
			if(result[0]['filename'] == search_text and
				result[0]['parent_folderkey'] == folder_key):
				return result[0]
		return {'result': 'different'}

	def get_info_file(self, quick_key):
		option = {}
		option['quick_key'] = quick_key
		option['session_token'] = self.__session_token.get_token()
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_INFO_FILE, option)
		if(js.get('result') == 'Error' and  not __debug__):
			print('Error in SystemOperation:get_info_file')
		return js['file_info']

	def delete_file(self, quick_key):
		js = self.get_json_mediafire(BaseUrlMediaFire.DELETE_FILE,
			{'session_token': self.__session_token.get_token(),
			'quick_key': quick_key,
			'version': self.__session_token.get_version_actual()})
		if (not __debug__):
			print(js)

	def move_file(self, quick_key, folder_key = None):
		option = {}
		option['session_token'] = self.__session_token.get_token()
		option['quick_key'] = quick_key
		if(folder_key is not None):
			option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.MOVE_FILE, option)
		if (not __debug__): 
			print(str(js) + " SystemOperation::move_file")

	def update_file(self, quick_key, option = {}):
		"""Update a file's information

		Keyword arguments:
			quick_key --  The quickkey that identifies the file
			option -- {} (defaul {})
				filename : The Name of the file (Should have same file type as the old file)
					The filename should be 3 to 255 in length
				description : The description of the file
				tags : A space-separated list of tags
				privacy : Privacy of the file ('public' or 'private')
				timezone : The code of the local timezone of the user.
		"""
		option['session_token'] = self.__session_token.get_token()
		option['quick_key'] = quick_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.UPDATE_FILE, option)
		if (not __debug__):
			print(str(js) + " SystemOperation::update_file")

	def update_password_file(self, quick_key, password):
		"""Update a file's password
		
		Keyword arguments:
			quick_key -- The quickkey that identifies the file
			password -- The new password to be set. To remove the password protection,
				pass an empty string
		"""
		js = self.get_json_mediafire(BaseUrlMediaFire.UPDATE_PASSWORD_FILE,
			{'session_token': self.__session_token.get_token(),
			'quick_key': quick_key,
			'password': password,
			'version': self.__session_token.get_version_actual()})
		if (not __debug__):
			print(str(js) + " SystemOperation::update_password")

#TODO
#	def change_quickkey(self, from_quickkey, to_quickkey):
#		"""Update a file's quickkey with another file's quickkey
#		Note: Only files with the same file extension can be used with this operation
#
#		Keyword arguments:
#			from_quickkey : The quickkey of the file to be overridden. After this operation,
#				this quickkey will be invalid
#			to_quickkey : The new quickkey that will point to the file previously identified
#				by from_quickkey.
#		"""
#		js = self.get_json_mediafire('http://www.mediafire.com/api/file/update_file.php',
#		{'session_token': self.__session_token.get_token(),
#		'from_quickkey': 'd75pi6ngg2ss38i',
#		'to_quickkey': 'atdfgt456ds2r6'})
#		if (not __debug__):
#			print(str(js) + " SystemOperation::change_quickkey")

	def copy_file(self, quick_key, folder_key = None):
		""" Copy a file to a specified folder. Any file can be copied whether it belongs to
		the session user or another user. However, the target folder must be owned by
		the session caller. Private files not owned by the session caller cannot be copied.

		Keyword arguments:
			quick_key -- The quickkey or a list of quickkeys that identify the files to be saved
			folder_key -- The key that identifies the destination folder. If omitted, the
				destination folder will be the root folder (My files) (defaul None)

		Return:
			new_quickkeys -- new quick_key of new file
		"""
		option = {}
		option['session_token'] = self.__session_token.get_token()
		option['quick_key'] = quick_key
		if(folder_key is not None):
			option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.COPY_FILE, option)
		if (not __debug__):
			print(str(js) + " SystemOperation::copy_file")  
		return js['new_quickkeys'][0]

	def copy_and_rename_file(self, new_name, quickkey, folder_key = None):
		ls = self.perfect_search(new_name,folder_key=folder_key)
		if(ls.get('result') == None):
			new_quickkeys = self.copy_file(quickkey, folder_key)
			self.update_file(new_quickkeys,{'filename':new_name})

	def cut_file(self,quickkey, folder_key = None): 
		self.copy_file(quickkey, folder_key)
		self.delete_file(quickkey)
		
	def get_links(self,quick_key, link_tipe = ''):
		"""Returns a list containing the view link, normal download link, and
		if possible the direct download link of a file. If the direct download
		link is not returned, an error message is returned explaining the reason
		
		Keyword arguments:
			quick_key -- The quickkey that identifies the file
			
			link_type : specify which link type is to be returned. If not 
				passed, all link types are returned. Values: 'view', 'edit',
				'normal_download', 'direct_download', 'one_time_download.' With
				the direct_download link, users have a free daily bandwidth of
				50 GB.(defaul '') 
			
		
		Return:
			{} -- normal_download, edit, direct_download, quickkey, 
				one_time_download
		"""
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_LINKS_FILE, 
			{'session_token': self.__session_token.get_token(),
			'quick_key': quick_key,
			'link_type': link_tipe,
			'version': self.__session_token.get_version_actual()})
		return js['links'][0]

	def one_time_download (self, quick_key, option = {}):
		option['session_token'] = self.__session_token.get_token()
		option['version'] = self.__session_token.get_version_actual()
		option['quick_key'] = quick_key
		js = self.get_json_mediafire(BaseUrlMediaFire.ONE_TIME_DOWNLOAD_FILE,
			option)
		return js

	def configure_one_time_download(self, token, option = {}):
		option['session_token'] = self.__session_token.get_token()
		option['version'] = self.__session_token.get_version_actual()
		option['token'] = token
		js = self.get_json_mediafire(
			BaseUrlMediaFire.CONFIGURE_ONE_TIME_DOWNLOAD_FILE, option)
		if not __debug__:
			print(str(js) + " SystemOperation::update_password")
		return js

	def get_info_folder(self, folder_key = None, option = {}):
		if(folder_key == None):
			option['session_token'] = self.__session_token.get_token()
		else:
			option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_INFO_FOLDER, option)
		return js['folder_info']

	def delete_folder(self, folder_key):
		js = self.get_json_mediafire(BaseUrlMediaFire.DELETE_FOLDER,
		{'session_token': self.__session_token.get_token(),
		'folder_key': folder_key,
		'version': self.__session_token.get_version_actual()})
		if not __debug__:
			print(str(js) + " SystemOperation::delete_folder")
		return js

	def move_folder(self, folder_key_src, folder_key_dst = None):
		option = {}
		option['session_token'] = self.__session_token.get_token()
		option['folder_key_src'] = folder_key_src
		if(folder_key_dst != None):
			option['folder_key_dst'] = folder_key_dst
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.MOVE_FOLDER, option)
		if(not __debug__):
			print(str(js) + 'SystemOperation::move_folder')
		return js

	def create_folder(self, foldername, option = {}):
		option['session_token'] = self.__session_token.get_token()
		option['foldername'] = foldername
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.CREATE_FOLDER, option)
		if(not __debug__):
			print(str(js) + 'SystemOperation::create_folder')
		return js

	def update_folder(self, folder_key, option = {}):
		option['session_token'] = self.__session_token.get_token()
		option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.UPDATE_FOLDER, option)
		if(not __debug__):
			print(str(js) + 'SystemOperation::update_folder')
		return js

	def rename_folder(self, folder_key, foldername):
		js = self.get_json_mediafire(BaseUrlMediaFire.UPDATE_FOLDER,
			{'foldername': foldername,
			'session_token' : self.__session_token.get_token(),
			'version': self.__session_token.get_version_actual(),
			'folder_key': folder_key})
		if(not __debug__):
			print(str(js) + 'SystemOperation::rename_folder')
		return js

	#TODO return access deneged 403 (bug)
	def attach_foreign(self, folder_keys):
		option = {}
		option['session_token'] = self.__session_token.get_token()
		option['folder_key'] = folder_keys
		js = self.get_json_mediafire(BaseUrlMediaFire.ATTACH_FOREIGN_FOLDER,option)
		return js

	#TODO return access deneged 403 (bug)
	def detach_foreign(self, folder_key):
		option = {}
		option['session_token'] = self.__session_token.get_token()
		option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.DETACH_FOREIGN_FOLDER,
			option)
		return js

	def get_revision_folder(self, folder_key):
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_REVISION_FOLDER,
			{'session_token':  self.__session_token.get_token(),
			'folder_key': folder_key,
			'version': self.__session_token.get_version_actual(),
			'return_changes': 'yes'})
		return js

	def  get_depth_folder(self, folder_key):
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_DEPTH_FOLDER,
			{'session_token': self.__session_token.get_token(),
			'folder_key': folder_key,
			'version': self.__session_token.get_version_actual()})
		if(not __debug__):
			print(str(js) + 'SystemOperation::get_revision_folder')
		return js['folder_depth']

	def get_siblings (self, folder_key, option = {}):
		print(self.__session_token.get_token())
		option['session_token'] = self.__session_token.get_token()
		option['folder_key'] = folder_key
		option['version'] = self.__session_token.get_version_actual()
		js = self.get_json_mediafire(BaseUrlMediaFire.GET_SIBLINGS_FOLDER,option)
		if(not __debug__):
			print(str(js) + 'SystemOperation::get_siblings')
		return js

	def pre_upload(self, filename, option = {}):
		option['session_token'] = self.__session_token.get_token()
		option['version'] = self.__session_token.get_version_actual()
		option['filename'] = filename
		js = self.get_json_mediafire(BaseUrlMediaFire.PRE_UPLOAD, option)
		return js
		

	def upload(self, filename, option = {}):
		user_agent = ('Mozilla/9.876 (X11; U; Linux 2.2.12-20 i686, en; rv:2.0) '
			'Gecko/25250101 Netscape/5.432b1 (C-MindSpring)')

		option['session_token'] = self.__session_token.get_token()
		option['version'] = self.__session_token.get_version_actual()
		option['response_format'] = 'json'
		
		get = urllib.parse.urlencode(option)
		fp = open(filename,'rb')
		form = MultiPartForm()
		form.add_file('fileUpload', filename, fileHandle=fp)

		form.make_result()
		url = BaseUrlMediaFire.UPLOAD + '?' + get
		req1 = urllib.request.Request(url)
		req1.add_header('User-Agent', user_agent,)
		req1.add_header('Content-type', form.get_content_type())
		req1.add_header('Content-length', len(form.form_data))
		req1.add_data(form.form_data)

		fp.close()
		try: response = urllib.request.urlopen(req1)
		except urllib.error.URLError as e:
			print(e)
			return json.loads('{"result":"Error"}')
		json_response = response.readall().decode('UTF-8')
		try: json_response = json.loads(json_response)['response']
		except ValueError:
			sys.stderr.write('Decoding JSON has failed in url \n\t' + url + '\n\n')
			return  json.loads(json_response)
		return json_response

	def poll_upload(self, key):
		js = self.get_json_mediafire(BaseUrlMediaFire.POLL_UPLOAD,
			{'key': key,
			'session_token' : self.__session_token.get_token(),
			'version': self.__session_token.get_version_actual()})
		if(not __debug__):
			print(str(js) + 'SystemOperation::poll_upload')
		return js


"""
Doug Hellmann's urllib2, translated to python3.
"""
class MultiPartForm():
	"""Accumulate the data to be used when posting a form."""

	def __init__(self):
		self.form_fields = []
		self.files = []
		self.form_data = None
		self.boundary = email.generator._make_boundary()
		return

	def get_content_type(self):
		return 'multipart/form-data; boundary=%s' % self.boundary

	def add_field(self, name, value):
		"""Add a simple field to the form data."""
		self.form_fields.append((name, value))
		return

	def add_file(self, fieldname, filename, fileHandle, mimetype=None):
		"""Add a file to be uploaded."""
		body = fileHandle.read()
		if mimetype is None:
			mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
		self.files.append((fieldname, filename, mimetype, body))
		return

	def make_result(self):
		"""Return bytes representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request. Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
		parts = []
		part_boundary = '--' + self.boundary

        # Add the form fields
		parts.extend(
			[ bytes(part_boundary, 'utf-8'),
			bytes('Content-Disposition: form-data; name="%s"' % name, 'utf-8'),
			b'',
			bytes(value, 'utf-8'),
			]
			for name, value in self.form_fields
			)

        # Add the files to upload
		parts.extend(
			[ bytes(part_boundary, 'utf-8'),
			bytes('Content-Disposition: file; name="%s"; filename="%s"' % (field_name, filename), 'utf-8'),
			bytes('Content-Type: %s' % content_type, 'utf-8'),
			b'',
			body,
			]
			for field_name, filename, content_type, body in self.files
			)

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
		flattened = list(itertools.chain(*parts))
		flattened.append(bytes('--' + self.boundary + '--', 'utf-8'))
		flattened.append(b'')
		self.form_data = b'\r\n'.join(flattened)

	#def __str__(self):
		#return str({'self.form_fields': self.form_fields, 'self.files': '{} pieces'.format(len(self.files)), 'self.boundary': self.boundary})

    # def __repr__(self):
    # return str({'self.form_fields': self.form_fields, 'self.files': '{} pieces'.format(len(self.files)), 'self.boundary': self.boundary})
        







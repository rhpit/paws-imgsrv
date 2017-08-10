Folder to save your windows libvirt images and files (QCOW and XML). 
The content of this folder is managed only when imgsrv is running on server. 
Any content saved here should not be pushed to git repo.

A valid image for PAWS QCOW Image Service is the combination of:
- .qcow ( it is the actual QCOW file exported from Openstack )
- .xml  ( it is the output from virsh dumpxml )
- .paws ( it is the output from PAWS provision task used to create the VM in 
		  Openstack and consequently the source for snapshot export )

example: a new QCOW image is extracted from Openstack for Windows_2016
to be a valid Image for PAWS QCOW Image Service and ready to be consumed
by PAWS for libvirt provider on the upload time it need:

windows_2012_R2.qcow
windows_2012_R2.paws
windows_2012_R2.xml

see .sample files 

--
test.xml and test.qcow are only needed to run unit tests suites. they can be
deleted if it is a non-devel environment 
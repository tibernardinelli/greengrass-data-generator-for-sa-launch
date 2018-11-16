#!/bin/sh

yum update -y

#Once connected to your Amazon EC2 instance through SSH, run the following commands to create user ggc_user and group ggc_group
adduser --system ggc_user
groupadd --system ggc_group

#Extract and run the following script to mount Linux control groups (cgroups). This is an AWS Greengrass dependency:
curl https://raw.githubusercontent.com/tianon/cgroupfs-mount/951c38ee8d802330454bdede20d85ec1c0f8d312/cgroupfs-mount > cgroupfs-mount.sh
chmod +x cgroupfs-mount.sh 
sudo bash ./cgroupfs-mount.sh

sudo yum install git -y
git clone https://github.com/aws-samples/aws-greengrass-samples.git
cd aws-greengrass-samples
cd greengrass-dependency-checker-GGCv1.6.0
sudo ./check_ggc_dependencies

aws s3 cp s3://greengrassd-files-sa-launch-team-3/greengrass-linux-x86-64-1.6.0.tar.gz /tmp/greengrass-linux-x86-64-1.6.0.tar.gz
tar -xzvf /tmp/greengrass-linux-x86-64-1.6.0.tar.gz -C /

aws s3 cp s3://greengrassd-files-sa-launch-team-3/certs/ThreathDetection_core.key /greengrass/certs/ThreathDetection_core.key
aws s3 cp s3://greengrassd-files-sa-launch-team-3/certs/ThreathDetection_core.pem /greengrass/certs/ThreathDetection_core.pem
aws s3 cp s3://greengrassd-files-sa-launch-team-3/certs/ThreathDetection_core.pub /greengrass/certs/ThreathDetection_core.pub
aws s3 cp s3://greengrassd-files-sa-launch-team-3/config/config.json /greengrass/config/config.json

cd /greengrass/certs/
sudo wget -O root.ca.pem http://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem

cd /greengrass/ggc/core/
sudo ./greengrassd start

# aws s3 sync config/ s3://greengrassd-files-sa-launch-team-3/config/
# aws s3 sync certs/ s3://greengrassd-files-sa-launch-team-3/certs/
# Real-Time Voice Cloning

This fork is for anyone who had trouble getting Corentin Jemine's original [project](https://github.com/CorentinJ/Real-Time-Voice-Cloning) up and running. Since it now has CPU support, much of the installation pain is resolved. Still, you might find this useful if you would like to generate many voice files.

With this repo, you can clone voices in the cloud using Amazon SageMaker. We won't implement the toolbox so there are no fancy visualizations and no GUI. But you will be able to get the functionality of `demo_cli.py` with minimal setup.

## Prerequisites

* An AWS account. We will be using resources that aren't available with free tier, i.e. P2 instances.
* A python installation with boto3. This is only needed if you want to run the sample notebook locally. You could also just do everything from a SageMaker notebook. But that would make this more expensive.

## Costs

Yes, AWS costs money. With this project though, running the example should cost you less than $1. If you want your voice clone read an entire novel or all of Wikipedia, that might be different story. In any case, it uses the following resources:
 
* *A SageMaker notebook instance* - This is only needed for installation / setup. Assuming this takes a full hour (which it shouldn't), you'll spend $0.0464 as of this writing.
* *S3 storage* - The model files, utterance files and results generated are less a GB. So this will only cost you a few pennies per month. 
* *ECR storage* - The container this creates will be ~3GB. So that's $0.30 per month.
* *Batch processing* - This is potentially expensive if you plan to run large jobs. The provided example should only take ~11 minutes. Using a CPU instance (ml.m5.large) at $0.134 per hour that comes to 11 / 60 * 0.134 = $0.02

I might experiment with different instance types in the future. For a large enough job, it might be more economical to use bigger or even GPU instances. But since about half of that 11 minutes is spent starting the container, it wouldn't help with the example notebook.

## Instructions

1. Create an S3 bucket. To do this, sign into the AWS console, go [here](https://s3.console.aws.amazon.com/s3/) and click "Create bucket". Give it a name and select a region. Rememeber the name you give it, since you'll need this later.

2. Create an ECR repository. Similarly, go [here](https://console.aws.amazon.com/ecr/) and click "Create repository". Use the same region as before and remember the name you give it.

3. Provision a SageMaker notebook instance. Go [here](https://console.aws.amazon.com/sagemaker/). Under "Notebook" -> "Notebook instances", click "Create notebook instance". Give it a name. Under "Notebook instance settings", "Additional configuration" increase the volume size to 50 GB. Under "Git repositories" select "Clone a public Git repository to this notebook instance only". Enter the URL of this repository. All other default settings should be fine.

4. Configure the install script to use your S3 bucket and ECR repository. Once the notebook instance is up and running, open Jupyter Lab and edit the copy of this [file](./scripts/install.sh). Enter the names you created for steps 1. and 2.

5. Run the install script. Installation will take several minutes to complete. From a terminal in Jupyter Lab, execute the following:

```
cd SageMaker/Real-Time-Voice-Cloning/scripts
chmod +x install.sh
./install.sh
```

6. Configure and run the sample [notebook](./example.ipynb). Enter your bucket name in the first cell. If everything is working, you should see this from the last cell after several minutes: 

```
Downloading: freeman_hp_0.wav
Downloading: freeman_hp_1.wav
Downloading: freeman_hp_2.wav
Downloading: freeman_hp_3.wav
Downloading: freeman_hp_4.wav
Downloading: freeman_hp_5.wav
Downloading: freeman_two_cities_0.wav
Downloading: freeman_two_cities_1.wav
Downloading: freeman_two_cities_2.wav
Downloading: vader_hp_0.wav
Downloading: vader_hp_1.wav
Downloading: vader_hp_2.wav
Downloading: vader_hp_3.wav
Downloading: vader_hp_4.wav
Downloading: vader_hp_5.wav
Downloading: vader_two_cities_0.wav
Downloading: vader_two_cities_1.wav
Downloading: vader_two_cities_2.wav
```

7. Running locally. If everything is working at this point, you can stop or even delete your SageMaker notebook. Assuming you have the AWS CLI installed and [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html), you can now run the sample notebook locally. The only python dependencies are boto3 and sagemaker. The batch processing job will still run in the cloud regardless.

## Model Training with SageMaker

I will get to this in the near future. It should be pretty straightforward to implement. But as of now this fork only has the functionality of `demo_cli.py`. In the mean time, you can check out [this](https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues/400) issue for a list of pretrained models.
# MotionEyeOS to AWS Rekognition

- Create an AWS bucket, and (preferably) an AWS IAM role with programatic access to write to the bucket. Save the API key and secret. 
- [Install MotionEyeOS](https://github.com/ccrisan/motioneyeos/wiki/Installation)
- [Grab the Golang s3-uploader source](https://github.com/artemnikitin/s3-uploader)
  - Cross-compile the source for the Pi device you're using. For example:
    - GOOS=linux GOARCH=arm GOARM=5 go get github.com/artemnikitin/s3-uploader
    - 5 for pi zero, 7 for pi 3. 
    - I did this in Docker, then just copied out ~/go/src/github.com/artemnikitin/s3-uploader
    - copy the s3-uploader binary to /data/bin on motioneyeos
- Copy the included wrapper script, upload.sh to /data/bin/upload.sh
  - Edit the AWS settings at the top of the script to the bucket, API key and secret you created earlier. 
- In MotionEyeOs, under "File Storage", enable "Run A Command," and set the "Command" to "/data/bun/upload.sh %f"
- In AWS, go to the Lambda console, under "Functions," click "Create a Function."
  - select "blueprints", search "rekognition"
  - use the "rekognition-python" blueprint
  - Name the function, and name the new role
  - Under "trigger", select your bucket, and the event type, "Object Created (All)"
  - optionally, add a prefix and/or file extension to limit to a particular path, and e.g. jpg uploads. 
  - click "enable trigger"
  - replace the function code with the code in this repo
  - click "create function" 
- In Telegram, send a message to @BotFather
  - send the command /newbot
  - give the bot a name
  - save the API token for later
  - send the command "/my_id" to @get_id_bot
  - save the chat id for later
- Back in the AWS console for your Lambda function, set these environment variables:
  - TELEGRAM_API_TOKEN
  - TELEGRAM_CHAT_ID
  - Optionally, set DEBUG to 1 to get more verbose output, and a message on every new upload, not just ones that look like people



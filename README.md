# Expense Tracker 

Some assembly required.

This application is a spending tracker/budgeter that monitors finances easily and quickly. The included Google Sheet template is also set up to help you keep track of your finances and easily see what categories are the ones you spend the most in. In order to sync this with your bank/card you must have email notifications enabled.

The basic flow for the application is as follows: purchase notifications via email are auto forwarded to an [Integromat](https://integromat.com) service. Integromat sends the email subject and body via a HTTP `POST` request to the Python Flask API endpoint. The API parses the transaction information (description/amount) from the email body, assigns it a category, and writes the transaction to the Google Sheets dashboard.

These instructions will walk you through how to set up the application for yourself and host it on Heroku. Fork and clone this repo to get started.


## Setup Email Purchase Notification
The secret API for all your financial accounts is purchase notifications. For each associated payment product, you need to turn on purchase notifications via email for any transaction you make. Follow your individual bank's instructions for this.

## Google Sheets Integration

### Setup Workbook
Copy the following [workbook](https://docs.google.com/spreadsheets/d/1PG5jfEHwhR_RoTvf9o7R82YdiVaM9TZ6AODpeC3TgJE/edit?usp=sharing) into your own Google drive. `File` > `Make a copy`. Make sure the copy is named `Budget`.

### Google Sheets API
Head to the [Google API Console](https://console.developers.google.com). You should see a box that says "To view this page, select a project." Click the `create` button the right side. Give it a name and save. Click the `Credentials` tab on the left side. Select `Create credentials` > `Service account key`.

Select `New service account` from the drop down. Give the service account a name, for the role enter `Project` > `Editor`. Keep `JSON` selected and create it. The credentials file will be automatically downloaded.  Rename this file `credentials.json` and move it to the this application's directory.

Next, select `Manage service accounts`. Copy the email address of the service account you just created. Head back to the Sheets workbook you copied and share the document with the service account email. Make sure to give it access to edit.

Go to the [Google Sheets API](https://console.developers.google.com/apis/api/sheets.googleapis.com/overview) and enable it for your project.

## Deploy to Heroku 
Create a free account on [Heroku](http://heroku.com/) if you don't already have one. [Download the Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).

Inside the application folder run 

```
heroku create my-app-name-here-api-heroku
```
`my-app-name-here` is the unique name of the application, change it to what ever you want. Heroku will assign a unique name for you if you don't put anything.

The output of the command should look like the following:

```
Creating ⬢ my-app-name-here-api-heroku... done
https://my-app-name-here-api-heroku.herokuapp.com/ | https://git.heroku.com/my-app-name-here-api-heroku.git
```

Take note of the base URL for the application as well as the Heroku git repo it creates for you. 

By default, Heroku deploys what ever is on the origin master branch in your fork to Heroku. However, we don't want to upload the `credentials.json` file to Github since that contains your Google account info. To fix this, we can create a local branch that contains `credentials.json` while your master does not. 

Create a new branch.

```
git checkout -b "secret-branch"
```

Now add and commit the `credentials.json` file.

```
git add credentials.json
git commit -m "Added credentials file"
```

Deploy by pulling any upstream changes from the master branch and then pushing to Heroku, Then check out the master branch again.

```
git pull origin master
git push heroku secret-branch:master
git checkout master
```

Check the Heroku logs to make sure your build succeeded.

```
heroku logs
```

## Configure Email auto-forwarding & Integromat

### Set Up Integromat
Login or create an account on [Integromat](https://integromat.com). Create a new Scenario. You'll need three modules: Custom Mailhooks, JSON Creation, HTTP Requests. Set anything you want for your email address prefix in the Custom Mailhook. Copy this email, click `Run Once`, and then head over to your email client, i.e. Gmail.

Send an email to your new email address with something in the subject and body. Head back to Integromat and once it receives your email, click the JSON module. You'll need to add a Data Structure, name it 'Email Content' and give it two items.

Use the following key-value pairs for the Data section.

```
body: Text
subject: Subject
```

Click `Ok` and then select the HTTP module. Enter the URL for the heroku app which should look something like 'https://your-app-name-here.herokuapp.com/budget/api/email'. Select 'POST' as the method and 'Raw' as the body type. Also select 'JSON (application/json)' as the content type. Finally, click on the 'Request content' box and select the JSON string. You should see the text you entered for the body and subject in the test email you sent.

Click 'Ok', save and then turn your scenario on.

### Auto-Forward emails to Integromat
Auto forward all of your purchase notifications to your new Integromat email address. For Gmail, instructions for setting up auto-forwarding with filtering for your specific messages can be found [here](https://support.google.com/mail/answer/10957?hl=en). 

## Parsing Purchase notifications
By default, the application is set up to parse Chase credit card purchase notifications and Venmo charge & payment notifications. If you want more/different integrations, you'll have to set them up yourself. The parsing of the purchase notifications is done via regex. 

The body of each request is set to print in the Heroku logs with `print(repr(body))`.  When an incoming purchase notification sent to the API, use the `Heroku logs` to view the logs and copy the raw email body, and then create a regex to parse the description and amount.  A helpful tool for building your regex expressions is [here](https://regex101.com/). Add a new `elif` block in the `parse_email()` function to capture this transaction type.


## Adding New Categories 
Each transaction is assigned a category based on the description that is parses from the email. Add the common places you buy things from the in the `constants.py`. Be sure to redeploy to Heroku once you make changes.

## Conclusion
Once set up this, this application offers a simple, unified view of your transaction history across all your payment methods. The only maintenance needed is if your credit card company decides to change the format of their purchase notification emails.  You'll have to update your regex, but this should be very infrequent.  

Because the app uses a Google Sheets workbook as the frontend and backend, it is customizable and open for you to do your own spending analysis.

# Innovaccer-summerGeeks
The website is live at: https://summer-geeks.herokuapp.com/

Please use above url to run the app. The uploaded code doesn't contain API keys and passwords, so to see the app in action quickly and save your time, please head to the link.

The main features of the app:
* The app multiple hosts to create meeting.
* One host can create multiple meetings but he cannot create meetings with same name.
* Host can manage the meeting and kick out any guest.
* The guest can check-in to any of the meetings.
* I have implemented token system for checking out and manage meetings

I have used Twilio's services for SMS. Their sms comes a little slow in our country (can take hours). Also, they send sms to verified numbers. So, I have verified a public number. You can see the sms generated here: https://www.receive-sms-online.info/917526812579-India along with other public messages. (If my free account's credits exhausts, sms won't come :( either way you can see my implementation.)


# How it Works?
- ## Tables
  There are three tables (models) that the project uses for storing and retreiving data.
   - ### Host
     The table consists data about hosts. Hosts can create and manage meeting. The fields in the table are: 
       * host_name
       * phone
       * email  
     `host_name` field stores the name of the host, submitted to the app when the meeting is created. `phone` field stores the phone      number of the host and `email` stores email of the host.
   - ### Meeting
      The table consists of meeting details created by hosts. Since, a host can create multiple meetings, we have a seperate table for meeting which consists of a foreign key pointing to host. The fields in the table are:
      * meeting_name
      * address
      * host
      * token  
     `meeting_name` and `address` field consists of the name and address of the meeting respectively. `host` is a foreign key to host table. `token` field consists of the token that is uniquely created for the meeting so that later, the host can use that unique token to manage the meeting. In the backend, the token in created sequentially and is unique for every meeting.
   - ### Guest
      The table consists of guest details that can join any meeting that is created. The fields are:
      * guest_name
      * guest_phone
      * guest_mail
      * checked_in
      * check_in_time
      * checked_out_time
      * meeting
      * token  
      `checked_in` is a boolean field that indicates, if the user has checked-in or not. In the app a guest can check-in to atmost one meeting. `check_in_time` and `checked_out_time` stores the time when the guest checked-in and checked-out to a meeting respectively. `meeting` field is a foreign key that points to a record in `Meeting table` (the meeting in which the guest has checked-in). `token` field stores the unique token for a user. The token is required when checking out of the meeting so that no one can check-out for someone else.
- ## Emails
  Emails are sent in the following scenarios:
  * **When the guest checks-out:** An email is sent to the guest to the email address that was provided when he checked-n to a meeting. The email consists all the details of the meeting along with the check-in and check-out time of the user.
  * **When the guest checks-in:** An email is sent to the host of the meeting mentioning the details about the guest who checked-in.
  * **When the guest is kicked out by the Host:** The email is also received by the guest in case he is kicked out by the host of the meeting. The emails states that the guest was checked out of the host and mentions all other details about the meeting.
      


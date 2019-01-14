# Starting up the application
Section 1: Using CS50 IDE, navigate to the folder in which the project is stored using the command cd finalproject, then execute flask run.

# Using the application
Section 2: Registering and Signing In

Upon reaching the website, the user should be directed to the login page. At this point, the user should register for a new account by clicking on the register link in the upper right-hand corner. The user should input a username, a password, and confirm the password (there are no password requirements). In the event that an account has already been created, you should log in using the username and password you created when registering.

Section 2.1: Homepage

After signing in, you should land on a page with a grey box containing the words "Top Study Sessions." This is the homepage for the website, and can be accessed at any time by clicking on the "StudySesh" logo located on the left side of the navbar located at the top of every page. Located underneath the grey box are the three highest rated active study sessions. Clicking on details will direct you to a page containing more detailed information about each study session (See section 2.3).

Section 2.2: Active Study Sessions

This page can be accessed by clicking on "Active Study Sessions" on the navbar at the top of any page. This page is a list of all currently active study sessions. Like each study session displayed on the homepage, every study session displayed here has an icon showing the location of the study session, the name of the study session with the rating for the session to the right of the name, and a location. Clicking on details will direct you to a page containing more detailed information about each study session (See section 2.3).

Section 2.3: Study Session Pages

This page has a number of elements. Underneath the name of the study session, the username of the user that created the study session, and its respective rating is an interactive Google Map showing the location of the study session. Underneath the map is a description of the study session. This page also contains a form through which users can leave reviews for the study session. Users are able to enter a numerical value between 1 and 5, and also leave a comment about the study session. Any existing reviews will appear in a table underneath this form. We intended for the comments section to be a way for users to get in touch with each other, regarding future study sessions. Upon leaving a review, users are currently redirected to the homepage.

Section 2.4: Map

This page can be accessed by clicking on "Map" on the navbar at the top of any page.This map displays the locations of all currently active study sessions. This map is not interactive.

Section 2.5: Make a Study Session

This page can be accessed by clicking on "Make a Study Session" on the navbar at the top of any page. This page is a form in which users can make their own study session. Users should fill out each field in this form, and will receive an alert if any field is blank. Name is the name of the user's study session, and is limited to 16 characters. Description is intended to be a brief description of the user's study session, but it can be as long as a user wishes. Building name is the name of the building the user's study session will take place in (e.g. Lamont Library), so long as the building is within the city of Cambridge. City name is restricted to Cambridge, and state name is restricted to Massachusetts.

Section 2.6: End a Study Session/Edit a Study Session

This page can be accessed by clicking on "Make a Study Session" on the navbar at the top of any page. This page is a table of any active sessions the user has created. If the status of any session is active, that means the session is active and displayed in active sessions, and if the status is inactive, that means the session is inactive and not displayed in active sessions. Users can end study sessions by clicking on the link labelled "End Session." This will remove the session from the list of active sessions featured on the "Active Study Sessions" page (see section 2.2). Users can edit study sessions by clicking on the links labelled "edit session." These links will direct users to a form. The name field is not editable, but users can update description and location of their study session.

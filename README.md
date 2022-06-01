# Project manager

A Flask app for easily saving workhours. The project is for University of Helsinki course Tietokantasovellus.

This app aims to make it easy to handle your work projects. It allows the user to use a stopwatch for saving workhours, comments for each session, choosing clients for projects etc.

A work-in-progress version can be tested in [Heroku](https://tsoha-project-manager.herokuapp.com)

## Development progress

### Login and register

Login system is mostly made without using packages like flask-login etc. Passwords are hashed using salted sha512 hashing algorithm. Login and new user registration system works fine, but probably will need some tweaks especially on the UI side.

### Main functionality

Main app GUI aims to be easy to use, especially requiring as few clicks as possible to do basic things.

## Planned features

- login to use app
- create and delete your projects
- time project using start/pause/stop, stop rounds time according to worktype
- stopwatch can be edited when ending session, if timer has been forgotten on or off
- add comments after working sessions
- finished (stopped) projects are not shown in default view, but can shown separately
- create and delete client companies and assing projects to them
- view statistics for different time ranges (matplotlib?)
- maybe export saved times in csv or some other format
- manually created worktypes to determine billing data (created by developer manually using sql)
- cancel started session (and project if empty)
- pause all projects easily using a single button in case of phonecalls or other interruptions
- restart project after saving it (creates new project with same functionality)
- when creating a project allow user to create it, create and start it, or create and stop, which automatically saves an entry with minimum time for that worktype

## Implementation

### Tables

At least these database tables will be used
- users(id, username, passwd)
- clients(id, name) maybe more columns later
- projects(id, status, comment, user_id, company_id, type_id)
- entries(id, project_id, starttime, endtime, comment)
- worktype(id, name, rounding, minimum, price)

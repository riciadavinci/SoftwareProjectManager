### Project Requirements (broad TODO list):
- [ ] Perform CRUD on SoftwareProjects
    - Fields: name, description, list of tasks, online resources, bugs, members
- [ ] Perform CRUD on Tasks (Project.id = foreign key)
    - Divided into 3 buckets: TODO, WIP, Done
    - timestamps for creation, modification
- [ ] Perform CRUD on OnlineResources (Project.id = foreign key)
- [ ] Perform CRUD on SoftwareBugs (Project.id = foreign key)
- [ ] Perform CRUD on Tasks (Project.id = foreign key)
- [ ] Perform CRUD on user
    - [ ] Add login and authentication with flask_login
    - [ ] Add various roles: Developer, Product Manager Role, Admin
- [ ] Generate a short PDF report for a project
    - [ ] Give analytics of tasks
    - [ ] List member contributions
    - [ ] Append list of online resources used as reference
    - [ ] Export the report to Markdown for Github


### Helpful Resources:
- [pytest Basics - playlist](https://www.youtube.com/playlist?list=PLxNPSjHT5qvuZ_JT1bknzrS8YqLiMjNpS)
- [Add Unit Tests to Flask App and API with Pytest](https://www.youtube.com/watch?v=3N2wm3nIuRE)
- [Testing Flask Applications with pytest - Patrick Kennedy](https://www.youtube.com/watch?v=OcD52lXq0e8)
- [Python Tutorial: Unit Testing Your Code with the unittest Module](https://www.youtube.com/watch?v=6tNS--WetLI)
- [Getting Started With Testing in Flask](https://www.youtube.com/watch?v=RLKW7ZMJOf4)


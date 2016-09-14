# HomePageV2 - fmars.me static to dynamic
HomePage_V1: Fetch static web page from Amazon S3

HomePage_V2: Back-end Python Flask, Front-end Javascript, Bootstrap, Apache2, Amazon EC2

## todo page feature lists:
- [ ] Create a independent one for todo which seperates TODO page out of hmoe page base 
- [ ] Each todo entry will have a few more fields. e.g. num of days, level (normal, hard, tough), auto email notification, etc.
- [ ] Auto simple score system for each entry and each user. Some rough idea is, for each user, default score per day is -1. 
Creating a todo will be 1. Succ or fail one entry will receive either position or negative of correspnding score which depends on the 
entry's level and num of days fields. Num of days should be exponetially corelated with score.
- [ ] Display user's statistic data such as todo entries created in last month, succ rate, etc.
- [x] Each user has icon photo
- [x] Along with more and more todo entries, we need pagedly render them
- [ ] Todo entry details hovercard shold be able to display backspace if user entered it when create the todo entry
- [ ] Should have some template to creat new todo entry instead of each time type the entire details once and once again
- [x] Test remote synch up functionality.

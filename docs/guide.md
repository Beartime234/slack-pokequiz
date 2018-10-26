---
layout: page
title: Guide
permalink: /guide/
---

Thanks for installing {{ site.quiz_name }}! Below are the instructions for using PokeQuiz
if you have any questions or experience any issues
feel free to contact me via the support email <a href="mailto:{{site.email}}">{{ site.email }}</a>

### Inviting PokeQuiz

After you install {{ site.quiz_name }} a bot named {{ site.bot_name }} will
be added to the workspace. By mentioning the bot or messaging the app directly
you can trigger quiz based commands. To mention the bot just type @{{ site.bot_name }}.
Before you can mention {{ site.bot_name }} you will need to invite the bot to your channel.
You can invite {{ site.bot_name }} through two methods. The first method is
mentioning {{ site.bot_name }} and then slackbot if enabled will as you if
you wish to invite them. Click invite them and you will then be able to
mention {{ site.bot_name}} Or you can open the sidebar of the channel and
click invite more people.

<img style="width: 60%; height: 60%;" src="{{ "/assets/images/inviting_bot.png" | relative_url }}">

### Help

After {{ site.bot_name }} has been invited to a channel you can ask for
some help just by mentioning {{ site.bot_name }} along with the word help.
For example you could say ```@{{ site.bot_name }} help me!```. {{ site.bot_name }}
will then give you some simple instructions. This may save you some time instead
of having to continuously visit this page.

<img style="width: 130%; height: 130%;" src="{{ "/assets/images/help.png" | relative_url }}">

### Starting a Quiz

After {{ site.bot_name }} has been invited to a channel you can start your
first quiz. To initiate a quiz with {{ site.bot_name }} just mention the bot
with the words quiz in it. For example you could say ```@{{ site.bot_name }}
quiz time``` or ```@{{ site.bot_name }} let's do a quiz!```. After this
your quiz will begin!

<img style="width: 50%; height: 50%;" src="{{ "/assets/images/starting_a_quiz.png" | relative_url }}">

### Answering a Question

Answering a question is very simple. All you need to do do is click the button which corresponds to the correct answer's number.
If you are correct or incorrect {{ site.bot_name }} will tell you and update the previous question with the incorrect and correct
answers. You can then choose to play again and get another question if you like.

<img style="width: 60%; height: 60%;" src="{{ "/assets/images/answering_a_question.gif" | relative_url }}">

### Leaderboard

In a similar way to starting a quiz you can request {{ site.bot_name }} to
show you the current leaderboard in the channel. Each time you answer correctly you get 1 point each incorrect answer takes away one point.
To show th leaderboard this mention {{ site.bot_name }} with the word leaderboard.
For example you could say ```@{{ site.bot_name }} show me the leaderboard```.
After this your channels leaderboard will be shown. Please note that this will mention each user on the leaderboard.

<img style="width: 60%; height: 60%;" src="{{ "/assets/images/leaderboard.png" | relative_url }}">

## Streaks

Each time you answer a question correctly your streak increases by one.
Whenever you answer a question incorrectly this resets your streak and you
will be informed of the streak you lost. You also get a special message whenever you
reach a multiple of 10 or 100 of your streak.

<img style="width: 60%; height: 60%;" src="{{ "/assets/images/streaks.png" | relative_url }}">
---
layout: page
title: Guide
permalink: /guide/
---

Thanks for installing {{ site.quiz_name }}! Below are the instructions for using PokeQuiz
if you have any questions feel free to contact me via the support email
located on the footer or raise an issue on Github!

### Inviting PokeQuiz

After you install {{ site.quiz_name }} a bot named {{ site.bot_name }} will
be added to the channel. By mentioning the bot you can trigger quiz based
commands. To mention the bot just type @{{ site.bot_name }}. Before you can
mention {{ site.bot_name }} you will need to invite the bot to your channel.
You can invite {{ site.bot_name }} through two methods. The first method is
mentioning {{ site.bot_name }} and then slackbot if enabled will as you if
you wish to invite them. Click invite them and you will then be able to
mention {{ site.bot_name}} Or you can open the sidebar of the channel and
click invite more people.

<img src="{{ "/assets/images/inviting_bot.png" | relative_url }}">

### Starting a Quiz

After {{ site.bot_name }} has been invited to a channel you can start your
first quiz. To initiate a quiz with {{ site.bot_name }} just mention the bot
with the words quiz in it. For example you could say ```@{{ site.bot_name }}
let's do a quiz``` or ```@{{ site.bot_name }} quiz time!```. After this
your quiz will begin!

<img src="{{ "/assets/images/starting_a_quiz.png" | relative_url }}">

### Answering a Question

Answering a question is very simple. All you need to do do is click the button which corresponds to the correct answer's number.
If you are correct or incorrect {{ site.bot_name }} will tell you and update the previous question with the incorrect and correct
answers. You can then choose to play again and get another question if you like.

<img src="{{ "/assets/images/answering_a_question.gif" | relative_url }}">

### Leaderboard

In a similar way to starting a quiz you can request {{ site.bot_name }} to
show you the current leaderboard in the channel. Each time you answer correctly you get 1 point each incorrect answer takes away one point.
To show th leaderboard this mention {{ site.bot_name }} with the word leaderboard.
For example you could say ```@{{ site.bot_name }} show me the leaderboard```.
After this your channels leaderboard will be shown. Please note that this will mention each user on the leaderboard.

<img src="{{ "/assets/images/leaderboard.png" | relative_url }}">

## Streaks

Each time you answer a question correctly your streak increases by one.
Whenever you answer a question incorrectly this resets your streak and you
will be informed of the streak you lost. You also get a special message whenever you
reach a multiple of 10 or 100 of your streak.

<img src="{{ "/assets/images/streaks.png" | relative_url }}">
---
layout: home
exclude_from_nav: true
---

# PokeQuiz

{{site.description}}

For information about {{ site.quiz_name }} see <a class="page-link" href="{{ "/about" | relative_url }}">about</a><br/>
For information on how to use {{ site.quiz_name }} see the <a class="page-link" href="{{ "/guide" | relative_url }}">guide</a>

<br/>
{%- if site.slack.client_id -%}
<a href="https://slack.com/oauth/authorize?scope=bot&client_id={{ site.slack.client_id }}"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
{%- endif -%}

<br/>
<br/>
<img style="width: 40%; height: 40%;" src="{{ "/assets/logo/pokequiz.png" | relative_url }}">

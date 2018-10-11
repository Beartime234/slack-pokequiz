---
# See: https://jekyllrb.com/docs/themes/#overriding-theme-defaults
layout: home
---

{{site.description}}

For more information see <a class="page-link" href="{{ "/about" | relative_url }}">about</a>

<br/>
{%- if site.slack.client_id -%}
<a href="https://slack.com/oauth/authorize?client_id={{ site.slack.client_id }}&scope=bot"><img alt="Add to Slack" height="50" width="180" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
{%- endif -%}

<br/>
<br/>
<br/>
<br/>

<img src="{{ "/assets/images/homepage.png" | relative_url }}">
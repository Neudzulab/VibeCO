# {{ project.get('name', 'Untitled Project') }}

> {{ project.get('tagline', 'Describe your project in one sentence.') }}

{% if project.get('status') %}**Current status:** {{ project['status'] | replace('_', ' ') | title }}
{% endif %}{% if project.get('owners') %}
**Owners**
{% for owner in project['owners'] %}- {{ owner.get('name', 'Owner') }}{% if owner.get('role') %} — {{ owner['role'] }}{% endif %}{% if owner.get('contact') %} (<{{ owner['contact'] }}>) {% endif %}
{% endfor %}{% endif %}

{% if project.get('overview') %}
## Overview
{% set overview = project['overview'] %}{% if overview.get('problem') %}- **Problem**: {{ overview['problem'] }}
{% endif %}{% if overview.get('solution') %}- **Solution**: {{ overview['solution'] }}
{% endif %}{% if overview.get('impact') %}- **Impact**: {{ overview['impact'] }}
{% endif %}{% endif %}

{% if project.get('values') %}
## Core Values
{% for value in project['values'] %}- **{{ value.get('name', 'Value') }}** — {{ value.get('description', '') }}
{% endfor %}{% endif %}

{% if project.get('experts') %}
## Expert Advisors
{% for expert in project['experts'] %}- **{{ expert.get('name', 'Expert') }}**{% if expert.get('speciality') %} ({{ expert['speciality'] }}){% endif %}: {{ expert.get('advice', 'Guidance forthcoming.') }}
{% endfor %}{% endif %}

{% if project.get('quality_gates') %}
## Quality Gates
{% for gate in project['quality_gates'] %}- **{{ gate.get('name', 'Gate') }}** — {{ gate.get('description', '') }}
{% endfor %}{% endif %}

{% if project.get('objectives') %}
## Objectives & Success Criteria
{% for objective in project['objectives'] %}
### {{ objective.get('title', 'Objective') }}
- **Status**: {{ objective.get('status', 'planned') | replace('_', ' ') | title }}
{% if objective.get('progress_percent') is not none %}- **Progress**: {{ objective['progress_percent'] }}%
{% endif %}{% if objective.get('next_keyword_holder') %}- **Next keyword holder**: {{ objective['next_keyword_holder'] }}
{% endif %}{% if objective.get('success_metrics') %}- **Success metrics**:
{% for metric in objective['success_metrics'] %}  - {{ metric }}
{% endfor %}{% endif %}{% if objective.get('notes') %}- **Notes**: {{ objective['notes'] }}
{% endif %}
{% endfor %}{% endif %}

{% if project.get('progress_updates') %}
## Progress Updates
| Date | Completion | Summary |
|------|------------|---------|
{% for update in project['progress_updates'] %}| {{ update.get('date', 'TBD') }} | {{ update.get('percent_complete', '0') }}% | {{ update.get('summary', '') }} |
{% endfor %}{% endif %}

{% if project.get('roadmap') %}
## Roadmap
| Milestone | Due date | Owner | Focus |
|-----------|----------|-------|-------|
{% for item in project['roadmap'] %}| {{ item.get('milestone', 'TBD') }} | {{ item.get('due', 'TBD') }} | {{ item.get('owner', 'TBD') }} | {{ item.get('focus', '') }} |
{% endfor %}{% endif %}

{% if project.get('artifacts') %}
## Reference Links
{% for name, link in project['artifacts'].items() %}- **{{ name | replace('_', ' ') | title }}**: {{ link }}
{% endfor %}{% endif %}

{% if project.get('notes') %}
## Additional Notes
{{ project['notes'] }}
{% endif %}

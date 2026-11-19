from collections import Counter
from datetime import datetime, timezone
import pandas as pd
import plotly.express as px
import streamlit as st
from jobradar.service import load_data, filter_jobs, summary, annual_pay, csv_export, DEFAULT_EXPERIENCE

st.set_page_config(page_title='Next Step | Bay Area Graduate Jobs',page_icon='↗',layout='wide')
st.markdown('''<style>
.stApp {background:#f7f9f8;color:#102f2a} [data-testid="stSidebar"]{background:#eaf1ee}
.block-container{padding-top:2.5rem;max-width:1440px} h1,h2,h3{letter-spacing:-.035em}
[data-testid="stMetric"]{background:#fff;border:1px solid #dce6e0;border-radius:12px;padding:18px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.16em;color:#16735a;margin-bottom:8px}
.intro{font-size:18px;max-width:780px;color:#557067;line-height:1.55}
.rule{height:1px;background:#dce6e0;margin:24px 0}
</style>''',unsafe_allow_html=True)

try: data=load_data()
except (FileNotFoundError,ValueError) as exc:
    st.error(str(exc)); st.code('python -m jobradar.ingest'); st.stop()
jobs=data['jobs']; meta=data['metadata']
checked=datetime.fromisoformat(meta['generated_at']); age_hours=(datetime.now(timezone.utc)-checked).total_seconds()/3600

st.markdown('<div class="eyebrow">NEXT STEP / BAY AREA / CLASS OF 2026</div>',unsafe_allow_html=True)
st.title('Find your first move.')
st.markdown('<div class="intro">Explore early-career opportunities across business and technology. Compare roles, places, pay, and skills—then go straight to the employer.</div>',unsafe_allow_html=True)
st.caption(f"Last source check: {checked.strftime('%b %d, %Y · %H:%M UTC')}  ·  {meta['sources_succeeded']} employer boards reached  ·  Public employer postings")
if age_hours>48: st.warning('This snapshot is more than 48 hours old. Openings may have changed. Check the employer link before applying.')
if meta['sources_failed']: st.warning(f"{meta['sources_failed']} employer feeds could not be refreshed. Any retained earlier listings from those sources are unverified and excluded by default.")

role_options=sorted({j['role_category'] for j in jobs})
with st.sidebar:
    st.header('Your search')
    q=st.text_input('Search jobs, employers, or skills',placeholder='e.g. analyst, SQL, Stripe')
    roles=st.multiselect('Career paths',role_options,default=[r for r in role_options if r!='Software & engineering'])
    st.caption('Starts with MIS and business paths. Add Software & engineering to broaden the search.')
    cities=st.multiselect('Locations',sorted({c for j in jobs for c in j['cities']}))
    exp=st.multiselect('Experience evidence',sorted({j['experience_status'] for j in jobs}),default=[x for x in DEFAULT_EXPERIENCE if any(j['experience_status']==x for j in jobs)])
    st.caption('Entry titles are a signal, not verified eligibility. Unknown experience is excluded by default.')
    arrangements=st.multiselect('Work arrangement',sorted({j['work_arrangement'] for j in jobs}))
    year=st.selectbox('Posting year',['2026','Any year'])
    cohort_choice=st.selectbox('Graduation eligibility',['No stated exclusion of 2026','Explicitly mentions 2026','All cohorts / review'])
    st.caption('No stated exclusion does not confirm that a 2026 graduate qualifies.')
    remote=st.checkbox('Include US remote with California eligibility unverified',value=False)
    statuses=st.multiselect('Listing status',['Listed at last check','No longer listed','Source unavailable — unverified'],default=['Listed at last check'])
    recent=st.selectbox('Posted within',['Any time','7 days','30 days','90 days'])
    salary_only=st.checkbox('Require disclosed annual USD pay')
    salary_floor=st.number_input('Minimum advertised lower bound ($/year)',min_value=0,max_value=500000,value=0,step=10000,disabled=not salary_only)
    closing=st.selectbox('Published application deadline',['Any / not specified','Within 7 days','Within 30 days'])
    st.caption('A missing deadline means the employer has not supplied one in this feed.')

filtered=filter_jobs(jobs,q=q,roles=roles,cities=cities or None,experience=exp,arrangements=arrangements or None,
    year=2026 if year=='2026' else None,cohort={'No stated exclusion of 2026':'compatible','Explicitly mentions 2026':'explicit','All cohorts / review':'all'}[cohort_choice],
    include_unverified_remote=remote,statuses=statuses,min_salary=salary_floor if salary_only else None,
    posted_within_days=int(recent.split()[0]) if recent!='Any time' else None,
    deadline_within_days=int(closing.split()[1]) if closing!='Any / not specified' else None)
stats=summary(filtered)
cols=st.columns(4)
for col,label,value in zip(cols,['Matching postings','Employers','Annual pay disclosed','Published deadlines'],
                          [f"{stats['jobs']:,}",stats['employers'],f"{stats['annual_pay_coverage_pct']:.0f}%",stats['published_deadlines']]): col.metric(label,value)
st.caption('Counts describe this selected set of postings, not all Bay Area vacancies or completed hires.')
st.markdown('<div class="rule"></div>',unsafe_allow_html=True)


def chart_style(fig):
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font={'family':'sans-serif','color':'#294d42'},
                      margin={'t':15,'b':15,'l':10,'r':35},height=335,showlegend=False)
    fig.update_xaxes(gridcolor='#e2eae5',zeroline=False); fig.update_yaxes(gridcolor='#e2eae5',zeroline=False)
    return fig


def bar(counter,label,color='#17745a',top=10):
    counts=pd.DataFrame(sorted(counter.items(),key=lambda x:x[1],reverse=True)[:top],columns=[label,'Postings']).sort_values('Postings')
    fig=px.bar(counts,x='Postings',y=label,orientation='h',text='Postings',color_discrete_sequence=[color])
    fig.update_traces(hovertemplate='%{y}<br>%{x} postings<extra></extra>',textposition='outside',cliponaxis=False)
    fig.update_xaxes(range=[0,max(counter.values())*1.2])
    st.plotly_chart(chart_style(fig),width='stretch',config={'displayModeBar':False})


if not filtered:
    st.info('No postings match this combination. Try Any year, fewer filters, or review jobs with experience not specified.')
else:
    left,right=st.columns(2,gap='large')
    with left:
        st.subheader('01 / Where your skills can lead')
        top_role=max(stats['roles'],key=stats['roles'].get)
        st.caption(f"{top_role} has the most matching postings ({stats['roles'][top_role]}).")
        bar(stats['roles'],'Career path')
    with right:
        st.subheader('02 / A place to get started')
        top_city=max(stats['cities'],key=stats['cities'].get)
        st.caption(f"{top_city} appears on {stats['cities'][top_city]} matching postings. Multi-location jobs can appear in multiple bars.")
        bar(stats['cities'],'Location',color='#4f7d93')
    left,right=st.columns(2,gap='large')
    with left:
        st.subheader('03 / What the listings pay')
        pay=annual_pay(filtered); counts=Counter(j['role_category'] for j in pay)
        eligible=[j for j in pay if counts[j['role_category']]>=5]
        st.caption('Advertised annual USD range midpoints by role; minimum 5 postings per group. These are not offers or total compensation.')
        if eligible:
            frame=pd.DataFrame([{'Career path':j['role_category'],'Midpoint':(j['salary_min']+j['salary_max'])/2,'Employer':j['company'],'Lower':j['salary_min'],'Upper':j['salary_max']} for j in eligible])
            fig=px.box(frame,x='Midpoint',y='Career path',orientation='h',points='all',hover_data=['Employer','Lower','Upper'],color_discrete_sequence=['#b58a39'])
            fig.update_xaxes(tickprefix='$',tickformat=',.0f'); st.plotly_chart(chart_style(fig),width='stretch',config={'displayModeBar':False})
            st.caption(f"{len(eligible)} postings plotted; {len(filtered)-len(pay)} have no comparable annual USD range. Ranges may cover multiple locations.")
        else:
            coverage=Counter('Annual USD range disclosed' if j in pay else 'Pay missing / not comparable' for j in filtered)
            bar(coverage,'Pay disclosure',color='#b58a39')
            st.caption(f"Only {len(pay)} of {len(filtered)} postings disclose a comparable annual USD range. No role group reaches five disclosures, so salary comparisons are withheld.")
    with right:
        st.subheader('04 / Skills worth exploring')
        st.caption('Distinct postings mentioning each skill. Mentions can be required, preferred, or descriptive; they are not all requirements.')
        if stats['skills']:
            bar(stats['skills'],'Skill',color='#7b6d9b')
            skill=max(stats['skills'],key=stats['skills'].get)
            st.caption(f"{skill} appears in {stats['skills'][skill]} of {stats['description_coverage']} available descriptions.")
        else: st.info('No tracked skill mentions in these descriptions.')

st.markdown('<div class="rule"></div>',unsafe_allow_html=True)
st.subheader('Explore the opportunities')
st.caption('Select a row to inspect the eligibility evidence. Apply links open the original employer posting.')
st.download_button('Download these results · CSV',csv_export(filtered),file_name='bay-area-grad-jobs.csv',mime='text/csv',disabled=not filtered)


def pay_label(j):
    if j['salary_min'] is None: return 'Not specified'
    return f"{j['salary_currency'] or ''} {j['salary_min']:,.0f}–{j['salary_max']:,.0f} / {j['salary_interval'] or 'unspecified'}"


if filtered:
    frame=pd.DataFrame([{'Employer':j['company'],'Role':j['title'],'Location':j['location'],'Experience':j['experience_status'],
                        'Advertised pay':pay_label(j),'Posted':(j['posted_at'] or '')[:10] or 'Not specified',
                        'Deadline':(j['deadline'] or '')[:10] or 'Not specified','Apply':j['url']} for j in filtered])
    selection=st.dataframe(frame,hide_index=True,width='stretch',height=430,on_select='rerun',selection_mode='single-row',
                           column_config={'Apply':st.column_config.LinkColumn('Employer link',display_text='View job')},key='job_table')
    if selection.selection.rows and selection.selection.rows[0]<len(filtered):
        chosen=filtered[selection.selection.rows[0]]
        with st.container(border=True):
            st.subheader(chosen['title']); st.write(f"{chosen['company']} · {chosen['location']}")
            st.write('**Experience evidence:**',chosen['experience_evidence'])
            st.write('**Graduation:**',chosen['cohort_status']); st.write('**Work arrangement:**',chosen['work_arrangement'])
            st.write('**Skills mentioned:**',', '.join(chosen['skills']) or 'None extracted')
            st.write('**Pay basis:**',chosen['salary_basis'])
            st.caption(f"{chosen['source']} · {chosen['status']} · checked {chosen['last_checked_at'][:19]} UTC")
            if chosen['url']: st.link_button('Open employer posting ↗',chosen['url'])

with st.expander('Data coverage, methodology & refresh status'):
    st.write(f"This snapshot checked {meta['raw_postings_checked']:,} source postings across {meta['sources_succeeded']} successful employer boards and retained {meta['candidate_records']:,} geographically relevant candidates for filtering.")
    st.write('The employer list is a selected sample. Results do not measure total market demand, applicant competition, or completed hires. Full-time status and eligibility must be verified on the original posting.')
    st.write('Experience uses deterministic text rules. Alternative degree routes, preferred requirements, and unclear wording may need manual review. Explicit senior titles and numeric requirements above two years are excluded. Missing requirements remain unknown.')
    st.write('City counts can overlap for multi-location postings. US-remote roles without California-specific location evidence are excluded by default. Pay uses stated ranges and never silently annualizes hourly wages. Skills are mentions, not verified mandatory qualifications.')
    st.write('The GitHub Actions workflow is configured for a daily refresh. It becomes active only after publishing the repository with Actions enabled. A failed source retains older records as unverified; a complete source failure preserves the last good dataset.')
    st.dataframe(pd.DataFrame(meta['source_reports']),hide_index=True,width='stretch')
    st.markdown('Employer discovery: [Headcount Labs](https://huggingface.co/datasets/HeadcountLabs/tech-jobs), October 19, 2026 snapshot, ODbL 1.0. Live metadata: public Greenhouse and Lever employer feeds. Employer descriptions are processed for annotations and are not reproduced in full.')
    st.caption('Built for Joshua Milstead · Part 1 · No chatbot, paid APIs, or applicant tracking.')

import * as React from 'react';
import '../css/Notes.css';
import '../css/Header.css';
import NoteCard from "./notes/NoteCard";

export default function Notes(props) {
    const notes = [
        {
            title: 'Known Bugs & Improvements',
            description: 'List of bugs & improvements I am currently aware of',
            items: [
                'Window Sizing',
                'Convenient Menus & Filtering',
            ],
            labels: [
                'Scaling of the Frontend components of this app are not perfect. Starts looking bad around 980 x 823 pixels in some areas.',
                'Dock menus to screen & allow for team specific filtering of all pages.',
            ],
            reasons: [
                'I need to spend more time learning CSS',
                'Needs planning...',
            ],
            descriptionLabel: 'Issue',
            reasonLabel: 'Reason',
        },
        {
            title: 'Resources',
            description: 'Acknowledgments & information regarding this app',
            items: [
                'NFL Player Data & Weekly stats',
                'Frontend Features',
                'Backend Features',
                'Source Code',
            ],
            labels: [
                'StatHead',
                'MUI X/React',
                'Django/Django Rest Framework',
                'GitHub',
            ],
            reasons: [
                'StatHead',
                'MUI X',
                'Django',
                'GitHub Repo',
            ],
            urls: [
                'https://stathead.com/football/',
                'https://mui.com/',
                'https://www.djangoproject.com/',
                'https://github.com/Tom-OLeary/FFLCompanion',
            ],

            descriptionLabel: 'Resource',
            reasonLabel: 'Link',
        },
        {
            title: 'Data Integrity',
            description: 'Missing Data Points & Potential Inaccuracies',
            items: [
                'Scoring',
                'Player Stats',
            ],
            labels: [
                'Points for fumbles & 2Pt Conversions',
                'Weekly stats before 2023',
            ],
            reasons: [
                'Affects calculations on trade comparisons & other live stats',
                'Can only generate results for 2023 season data. ' +
                'Remaining data will need to be imported when I determine a more convenient way to do so.',
            ],
            descriptionLabel: 'Missing Data',
            reasonLabel: 'Result',
        },
        {
            title: 'Features',
            description: 'Features under consideration for future updates',
            items: [
                'Start/Sit Analyzer',
                'Rosters',
                'My Team Page',
                'Trade Machine',
                'Polls',
            ],
            labels: [
                'Calculate points gained from starters vs. players left on the bench.',
                'Link players to Team Owners for each season.',
                'Allow self imports of weekly scoring for live updates.',
                'Determine pros & cons of a potential trade offer.',
                'Allow user generated polls',
            ],
            reasons: [
                'Need to manually import lineup data for each week.',
                'Data needs to be gathered & imported. Model for Rosters already created.',
                'Planning in progress...',
                'Not sure how yet, but its coming someday.',
                'Its on the list.',
            ],
            descriptionLabel: 'Purpose',
            reasonLabel: 'Current Blocker',
        }
    ]
  return (
      // TODO work in progress
      <div style={{marginTop: 150}}>
          <h1 className="notes-page-title">NOTES</h1>
          <div className="center-page note-column">
              <NoteCard {...notes[0]} />
              <NoteCard {...notes[1]} />
              <NoteCard {...notes[2]} />
          </div>
          <div className="center-page note-column">
              <NoteCard {...notes[3]} />
          </div>
      </div>
  );
}
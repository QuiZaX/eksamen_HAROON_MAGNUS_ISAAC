document.addEventListener('DOMContentLoaded', () => {
    const groupsContainer = document.getElementById('groups');
    const knockoutContainer = document.getElementById('knockout-teams');

    // Sample data to simulate backend responses
    const groupResults = {
        'Group 1': [
            {team: 'Team A', points: 6},
            {team: 'Team B', points: 4},
            {team: 'Team C', points: 2},
            {team: 'Team D', points: 0}
        ],
        'Group 2': [
            {team: 'Team E', points: 6},
            {team: 'Team F', points: 4},
            {team: 'Team G', points: 2},
            {team: 'Team H', points: 0}
        ]
    };

    const knockoutTeams = ['Team A', 'Team B', 'Team E', 'Team F'];

    function updateGroups() {
        groupsContainer.innerHTML = '';
        for (const [groupName, standings] of Object.entries(groupResults)) {
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('group');
            const groupTitle = document.createElement('h2');
            groupTitle.textContent = groupName;
            groupDiv.appendChild(groupTitle);

            const leaderboard = document.createElement('ul');
            leaderboard.classList.add('leaderboard');

            standings.forEach(({team, points}) => {
                const listItem = document.createElement('li');
                listItem.textContent = `${team} - ${points} points`;
                leaderboard.appendChild(listItem);
            });

            groupDiv.appendChild(leaderboard);
            groupsContainer.appendChild(groupDiv);
        }
    }

    function updateKnockoutStage() {
        knockoutContainer.innerHTML = '';
        knockoutTeams.forEach(team => {
            const listItem = document.createElement('li');
            listItem.textContent = team;
            knockoutContainer.appendChild(listItem);
        });
    }

    // Initial update
    updateGroups();
    updateKnockoutStage();

    // Simulate dynamic updates
    setTimeout(() => {
        // Update group results
        groupResults['Group 1'][1].points = 7; // Team B gets more points
        updateGroups();

        // Update knockout teams
        knockoutTeams.push('Team C');
        updateKnockoutStage();
    }, 5000);
});

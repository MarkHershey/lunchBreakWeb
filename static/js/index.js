document.addEventListener('DOMContentLoaded', function (e) {
    const team_select = document.getElementById('team_select');
    const team_selected = document.getElementById('team_selected');

    team_select.addEventListener('change', updateTeamMembers);

    function updateTeamMembers(e) {
            team_selected.textContent = e.target.value;
        }
  })

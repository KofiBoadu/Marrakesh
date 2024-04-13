





function show_exportButton(){
	document.getElementById('export_form').style.display='block';
	
}

function closeExportModal(){
	document.getElementById('export_form').style.display='None';
}


function show_importButton(){
	document.getElementById('import_form').style.display='block';
	
}

function closeimportModal(){
	document.getElementById('import_form').style.display='None';
}


document.addEventListener('DOMContentLoaded', function() {
	const roleId = parseInt(document.getElementById('login-user-role-id').value, 10);
	if (roleId > 1) {
	  const exportButton = document.querySelector('.export');
	  if (exportButton) {
		exportButton.disabled = true;
		exportButton.classList.add('disabled'); // Use 'disabled' class for styling
		exportButton.style.backgroundColor ="#d3d3d357"
		exportButton.style.border="none"
		exportButton.innerHTML = '<img src="https://img.icons8.com/material-rounded/10/FF914C/lock-2.png" alt="Export icon"> Export';
	  }
	}
  });
  
function showLoader(type="bg-blue",message="En cours..."){
	$('#ajax-loader').modal()
	
	$('#loader span').html(message);
	$('#loader').removeClass().addClass(type);
	
	$('#loader').show();
}

function hideLoader(){
	$('#ajax-loader').modal('hide');
	$('#loader').hide();
}

function showError(message="Une erreur est survenue", title="Oops..."){
	swal({
	    title: title,
	    text: message,
	    confirmButtonColor: "#EF5350",
	    type: "error"
	});
}
function showConfirm(message="", title="Confirmation", is_confirm=false) {
    swal({
        title: title,
        text: message,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Valider',
        cancelButtonText: "Annuler",
        closeOnConfirm: true,
        closeOnCancel: true
    },
    function(isConfirm) {
        
        if (isConfirm == true){
            is_confirm = true
            console.log("la valeur de isConfirm: ",is_confirm)
        }
    })
    return is_confirm
}

function showInfo(message="Action termine avec succes", title="Infos"){
	swal({
	    title: title,
	    text: message,
	    confirmButtonColor: "#2196F3",
	    type: "info"
	});
}


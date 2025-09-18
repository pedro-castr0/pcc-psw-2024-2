$(function(){

    $(".abrir-denuncia").on("click", function(e){
        e.preventDefault();

        const objectId = $(this).data("object-id");
        const divForm = $(`#form-denuncia-${objectId}`);
        const url = $(this).data("url");

        $(".form-denuncia").not(divForm).hide();

        if(divForm.is(":visible")) { 
            divForm.hide(); 
            return; 
        }

        $.get(url, function(response){
            console.log(response);
            if(response.html){
                divForm.html(response.html).show();
            } else {
                divForm.html('<div class="text-danger">Erro ao carregar formulário</div>').show();
            }
        }).fail(function(xhr){
            console.log(xhr);
            divForm.html('<div class="text-danger">Erro ao carregar formulário</div>').show();
        });
    });

    $(document).on("submit", ".ajax-denuncia", function(e){
        e.preventDefault();

        const form = $(this);
        const divForm = form.closest(".form-denuncia");
        const url = divForm.prev(".abrir-denuncia").data("url");

        $.post(url, form.serialize(), function(response){
            console.log(response);
            if(response.mensagem){
                alert(response.mensagem);
                divForm.hide();
            } else if(response.erro){
                alert(response.erro);
            }
        }).fail(function(xhr){
            console.log(xhr);
            alert(xhr.responseJSON?.erro || "Erro ao enviar denúncia.");
        });
    });

});

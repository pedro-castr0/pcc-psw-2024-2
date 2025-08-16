$(function(){

    // Abrir formulário de denúncia via AJAX
    $(".abrir-denuncia").on("click", function(e){
        e.preventDefault();

        const divForm = $(`#form-denuncia-${$(this).data("object-id")}`);
        $(".form-denuncia").not(divForm).hide();

        if(divForm.is(":visible")) { 
            divForm.hide(); 
            return; 
        }

        const url = $(this).data("url");  // pega a URL gerada pelo template

        $.get(url, function(response){
            divForm.html(response.html).show();
        }).fail(function(xhr){
            alert(xhr.responseJSON?.erro || "Erro ao carregar formulário.");
        });
    });

    // Delegar submissão do formulário AJAX
    $(document).on("submit", ".ajax-denuncia", function(e){
        e.preventDefault();

        const form = $(this);
        const divForm = form.closest(".form-denuncia");
        const url = divForm.prev(".abrir-denuncia").data("url"); // pega a URL via data-url

        $.post(url, form.serialize(), function(response){
            alert(response.mensagem);
            divForm.hide();
        }).fail(function(xhr){
            alert(xhr.responseJSON?.erro || "Erro ao enviar denúncia.");
        });
    });

    // Fechar clicando fora
    $(document).on("click", function(event){
        if(!$(event.target).closest('.form-denuncia, .abrir-denuncia').length){
            $(".form-denuncia").hide();
        }
    });

});

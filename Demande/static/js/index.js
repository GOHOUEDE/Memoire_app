document.addEventListener('DOMContentLoaded',function()
{
const rows =document.querySelectorAll('#dataTable tr[dm-url]');
rows.forEach (row =>
    {
        row.addEventListener ('click', function() {
            const url= this.getAttribute('dm-url');
            if(url){
                window.location.href = url;
            }
        });
    });
});
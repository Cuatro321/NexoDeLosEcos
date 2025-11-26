document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input,select,textarea').forEach(el=>{
    el.addEventListener('focus',()=>el.style.boxShadow='0 0 0 2px rgba(96,165,250,.35)');
    el.addEventListener('blur',()=>el.style.boxShadow='none');
  });
});

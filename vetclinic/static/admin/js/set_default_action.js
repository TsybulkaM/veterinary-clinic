document.addEventListener('DOMContentLoaded', function () {
    const actionSelects = document.querySelectorAll('select[name="action"]');
    actionSelects.forEach(select => {
        if (select.options.length > 1) {
            for (let i = 0; i < select.options.length; i++) {
                if (select.options[i].text === 'Verify and process selected requests') {
                    select.selectedIndex = i;
                    break;
                }
            }
        }
    });
});

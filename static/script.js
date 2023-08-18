document.addEventListener("DOMContentLoaded", function() {

    var select1_level = document.getElementById("select1_level");
    var select2_industry = document.getElementById("select2_industry");


    select1_level.addEventListener("change", function() {
        // 기존 옵션들을 모두 제거합니다.
        while (select2_industry.firstChild) {
            select2_industry.removeChild(select2_industry.firstChild);
        }

        // select1의 값에 따라 select2의 옵션들을 동적으로 추가합니다.
        if (select1_level.value === "2") {
            industries_level2.forEach(function(option) {
                let optionElement = document.createElement('option');
                optionElement.textContent = option;
                optionElement.value = option;
                select2_industry.appendChild(optionElement);
            });

        } else if (select1_level.value === "3") {
            industries_level3.forEach(function(option) {
                let optionElement = document.createElement('option');
                optionElement.textContent = option;
                optionElement.value = option;
                select2_industry.appendChild(optionElement);
            });

        } else if (select1_level.value === "4") {
            industries_level4.forEach(function(option) {
                let optionElement = document.createElement('option');
                optionElement.textContent = option;
                optionElement.value = option;
                select2_industry.appendChild(optionElement);
            });

        }


    });



});
const Meses_Label = [
          'Enero',
          'Febrero',
          'Marzo',
          'Abril',
          'Mayo',
          'Junio',
          'Julio',
          'Agosto',
          'Septiembre',
          'Octubre',
          'Noviembre',
          'Diciembre'
        ];

const Meses_django = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
    'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];


let indiceMes = 11;

function capitalizeWord(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

function inicializar_meses(){
    const diccionario = {};
    Meses_django.forEach(mes => {
        diccionario[mes] = 0;
    });
    return diccionario
}

function months_label(mes_actual) {
    return Meses_Label.slice(0, mes_actual)
}

/* Funcion para devolver una lista con la cantidad de ismn o inscrip rechazadas
de acorde al mes donde se encuentre el chart */
function extraer_organizar_datos(mes, inscrip_rechazados, ismn_rechazados){
    let inscrip_rechazados_mes_anterior = inscrip_rechazados['2023'][Meses_django[mes]];
    let ismn_rechazados_mes_anterior = ismn_rechazados['2023'][Meses_django[mes]];
    return [inscrip_rechazados_mes_anterior, ismn_rechazados_mes_anterior];
}


function addData(chart, inscrip_rechazados, ismn_rechazados) {
    let newData = extraer_organizar_datos(indiceMes, inscrip_rechazados, ismn_rechazados)
    if (chart.data.labels.length < 14){
        chart.data.labels.unshift(Meses_Label[indiceMes]);
        chart.data.datasets[0].data.unshift(newData[0]);
        chart.data.datasets[1].data.unshift(newData[1]);
        indiceMes = (indiceMes -1 + Meses_Label.length) % Meses_Label.length;
    }
    chart.update();
}

function removeData(chart) {
    if (chart.data.labels.length > 4){
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        indiceMes++;
    }
    chart.update();
}


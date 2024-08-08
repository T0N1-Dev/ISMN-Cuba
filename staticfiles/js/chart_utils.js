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
let indiceLabel = 1;
let indiceDataBarChart = 8;
let barChart_total = 0;

function sumaElementos(arreglo1, arreglo2) {
    let sumaTotal = 0;

    for (let i = 0; i < arreglo1.length; i++) {
        sumaTotal += arreglo1[i] + arreglo2[i];
    }
    return sumaTotal;
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

function agregarUltimoLabelAlPrincipio(listaOriginal) {
    let ultimo_elemento = listaOriginal[listaOriginal.length-indiceLabel];
    indiceLabel++;
    let newLabel = listaOriginal;
    newLabel.unshift(ultimo_elemento)
    return newLabel
}


function addDataLineChart(chart, inscrip_rechazados, ismn_rechazados) {
    let newData = extraer_organizar_datos(indiceMes, inscrip_rechazados, ismn_rechazados)
    if (chart.data.labels.length < 17){
        chart.data.labels.unshift(Meses_Label[indiceMes]);
        chart.data.datasets[0].data.unshift(newData[0]);
        chart.data.datasets[1].data.unshift(newData[1]);
        indiceMes = (indiceMes -1 + Meses_Label.length) % Meses_Label.length;
    }
    chart.update();
}

function removeDataLineChart(chart) {
    if (chart.data.labels.length > 5){
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        indiceMes = (indiceMes +1 + Meses_Label.length) % Meses_Label.length;
    }
    chart.update();
}

function addDataBarChart(chart, inscrip_enviados, ismn_enviados){
    let newInscripData = Object.values(inscrip_enviados).slice(-indiceDataBarChart);
    let newISMNData = Object.values(ismn_enviados).slice(-indiceDataBarChart);
    if (chart.data.labels.length < 30){
        chart.data.labels = agregarUltimoLabelAlPrincipio(chart.data.labels);
        chart.data.datasets[0].data = newInscripData;
        chart.data.datasets[1].data = newISMNData;
        indiceDataBarChart++;
        barChart_total = sumaElementos(newInscripData, newISMNData)
        chart.options.plugins.title.text = `Total: ${barChart_total}.`;
    }
    chart.update();
}

function removeDataBarChart(chart){
    if (chart.data.labels.length > 7) {
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        indiceDataBarChart--;
        indiceLabel--;
        barChart_total = sumaElementos(chart.data.datasets[0].data, chart.data.datasets[1].data);
        chart.options.plugins.title.text = `Total: ${barChart_total}.`;
    }
    chart.update();
}

function saveChart(pChartBar){
    let canvas_line_chart = document.getElementById('myChart');
    let canvas_bar_chart = document.getElementById('myChart2');
    let dataURL_lineChart = canvas_line_chart.toDataURL(); // Obtiene la representación base64 de la imagen
    let dataURL_barChart = canvas_bar_chart.toDataURL();
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Envía la imagen al servidor
    fetch('http://127.0.0.1:8000/export_statistics_solicitud', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ image_data_lineChart: dataURL_lineChart, image_data_barChart: dataURL_barChart,
                                    total_image_data_barChart: pChartBar.options.plugins.title.text}),
    }).then(response => {
        if (response.ok) {
            response.blob().then(blob => {
                // Crea un objeto URL para el archivo blob y lo descarga
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Estadísticas_solicitudes.pdf';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            });
        } else {
            console.error('Error al guardar la imagen:', response.statusText);
        }
    }).catch(error => {
        console.error('Error al guardar la imagen:', error);
    });
}

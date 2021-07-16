// $(document).ready(function(){
//     $('form').on('submit', function(event) {
//         $.ajax({
//             data : {
//                 name : $('#inputText').val(),
//             },
//             type : "POST",
//             url : '/process'
//         })
//         .done(function(data){
//             if (data.error){
//                 $('#errorAlert').text(data.error).show();
//                 $('#successAlert').hide();
//             } 
//             else {
//                 $('#successAlert').text(data.name).show();
//                 $('#errorAlert').hide();

//             }
//         });
//         event.preventDefault();
//     });
// });

// function addFields(){
//     var number = document.getElementById("member").value;
//     var container = document.getElementById("container");
//     var input = document.createElement("input");
//     input.type = "text";
//     input.value = document.getElementById("member").value;
//     //calculate the pairs
//     var text_input = document.createElement("text_input");
//     text_input.type = "text";
//     var text_input = document.getElementById("member").value;
//     console.log(input);
//     var neighbour_count = {};
//     var words = text_input.split(" ");
//     for (const [index, element] of words.entries()) {
//         if (index + 1 < words.length) {
//             var wordPair = [];
//             if (element > words[index + 1]) {
//                 var wordPair = [element, words[index + 1]]
//             } else {
//                 var wordPair = [words[index + 1], element]
//             }
//             console.log(wordPair)
//             if (wordPair in neighbour_count) {
//                 neighbour_count[wordPair] += 1
//             } else {
//                 neighbour_count[wordPair] = 1
//             }
//         }
//     }
//     container.appendChild(document.createElement("br"));
//     container.appendChild("2");
//     container.appendChild(neighbour_count);
//     //container.appendChild(typeof input);
//     console.log(neighbour_count);
//     container.appendChild(document.createElement("br"));
    
// }

let base64Image
$("#img").change(function () {
  reader = new FileReader();
  reader.onload = function (e) {
    let dataURL = reader.result
    $("#selected-img").attr("src", dataURL)
    base64Image = dataURL.replace("data:image/jpeg;base64", "")
    console.log(base64Image)
  }
  reader.readAsDataURL($("#img")[0].files[0]);
  $(".pred-output").text("")
})

const swiper = new Swiper('.swiper', {
    loop: true,
    speed: 700,
    autoplay: true
})

$("#submit").click(function (e) {
  const message = {
    image: base64Image,
  };
  console.log(message)
  $.post(
    "http://127.0.0.1:5000/predict",
    JSON.stringify(message),
    function (response) {
        console.log(response)
        $("#dog-pred").text(response.prediction.dog.toFixed(4));
        $("#cat-pred").text(response.prediction.cat.toFixed(4));
    }
  );
});

    $(document).ready(function() {
        var i = 1;
        $('.add').on('click', function() {
            var field = '<div><br><input type="text" name="grade">&nbsp<input type="text" name="score">&nbsp<span class="fa fa-minus remove"></span></div>';
            $('.appending_div').append(field);
            i = i + 1;
        });

        // Handle removal of fields
        $('.appending_div').on('click', '.remove', function() {
            $(this).parent().remove();
        });

        $('#advanced-test-form').submit(function(event) {
            event.preventDefault();
            var gradesList = [];
            $('.appending_div div').each(function() {
                var percentage = $(this).find('input[name="score"]').val();
                var grade = $(this).find('input[name="grade"]').val();
                if (percentage && grade) {
                    gradesList.push({
                        "percentage": parseInt(percentage),
                        "grade": grade
                    });
                }
            });

            var gradesData = {
                "grades": gradesList
            };

            // Convert gradesData to a JSON string and add it to a hidden field in the form
            var gradesDataJson = JSON.stringify(gradesData);
            $('<input>').attr({
                type: 'hidden',
                name: 'grades_data',
                value: gradesDataJson
            }).appendTo('#advanced-test-form');

            // Now submit the form with the grades data included
            $('#advanced-test-form').unbind('submit').submit();
        });



    });

$(document).ready(function() {
  const totalPages = $(".page").length;
  let currentPage = parseInt($("#current-page").val());

  // Function to show the current page and hide others
  function showPage(pageNumber) {
    $(".page").hide();
    $(`.page[data-page='${pageNumber}']`).show();
    $("#current-page").val(pageNumber);

    // Show or hide the submit button based on the current page
    if (pageNumber === totalPages) {
      $("#submit-btn").show();
    } else {
      $("#submit-btn").hide();
    }
  }

  // Function to navigate to the next page
  $("#next-page").click(function() {
    if (currentPage < totalPages) {
      currentPage++;
      showPage(currentPage);
    }
  });

  // Function to navigate to the previous page
  $("#prev-page").click(function() {
    if (currentPage > 1) {
      currentPage--;
      showPage(currentPage);
    }
  });

  // Show the initial page
  showPage(currentPage);
});

  $(document).ready(function() {
    // Function to calculate the total number of questions and update the "Total Questions" text
    function calculateTotalQuestions() {
      let totalQuestions = 0;
      $('.question-type').each(function() {
        const value = parseInt($(this).val());
        if (!isNaN(value)) {
          totalQuestions += value;
        }
      });
      $('#total-questions').text(totalQuestions);
      return totalQuestions;
    }

    // Call the function initially to set the initial value of "Total Questions"
    let totalQuestions = calculateTotalQuestions();

    // Bind the input event to each "Question Types" field to recalculate the total when any of them changes
    $('.question-type').on('input', function() {
      totalQuestions = calculateTotalQuestions();
    });

    // Function to handle keypress events and reject non-numeric input
    $('.question-type').on('keypress', function(event) {
      const charCode = event.which ? event.which : event.keyCode;
      // Allow only numbers, backspace, and delete keys
      if (charCode !== 8 && charCode !== 0 && (charCode < 48 || charCode > 57)) {
        event.preventDefault();
      }
    });

    // Form submission event
    $('#advanced-test-form').on('submit', function(event) {
      if (totalQuestions > 150) {
        // Show the error message and prevent form submission
        $('#error-message').show();
        event.preventDefault();
      } else {
        // Hide the error message if total questions are within the limit
        $('#error-message').hide();
      }
    });
  });

// Keep track of uploaded file contents
const uploadedFiles = [];

// Handle drag and drop events for the file input
const fileDropArea = document.querySelector('.file-drop-area');

fileDropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  fileDropArea.classList.add('file-drop-active');
});

fileDropArea.addEventListener('dragleave', () => {
  fileDropArea.classList.remove('file-drop-active');
});

fileDropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  fileDropArea.classList.remove('file-drop-active');

  const file = event.dataTransfer.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    // Update the textarea with the content of the dropped file
    const teachingMaterialTextarea = document.getElementById('teaching-material');
    teachingMaterialTextarea.value += '\n\n' + e.target.result;

    // Add the file content to the uploadedFiles array
    uploadedFiles.push(e.target.result);
  };

  reader.readAsText(file);
});

// Handle file input change event
document.getElementById('file-input').addEventListener('change', function (event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
    // Update the textarea with the content of the selected file
    const teachingMaterialTextarea = document.getElementById('teaching-material');
    teachingMaterialTextarea.value += '\n\n' + e.target.result;

    // Add the file content to the uploadedFiles array
    uploadedFiles.push(e.target.result);
  };

  reader.readAsText(file);
});

// Handle changes in the textarea (e.g., if the user deletes text)
document.getElementById('teaching-material').addEventListener('input', function (event) {
  const teachingMaterialTextarea = event.target;
  // Update the uploadedFiles array with the textarea content
  uploadedFiles.length = 0;
  const lines = teachingMaterialTextarea.value.split('\n');
  lines.forEach(line => {
    if (line.trim() !== '') {
      uploadedFiles.push(line);
    }
  });
});











$(document).ready(function() {
    var i = 1;
    var maxGrades = 6; // Set the maximum number of grades fields

    // Disable the "Add" button if the maximum limit is reached
    if (i >= maxGrades) {
        $('.add').prop('disabled', true);
    }

    $('.add').on('click', function() {
        if (i < maxGrades) {
            var field = '<div><br><input type="text" name="grade">&nbsp<input type="text" name="score">&nbsp<span class="fa fa-minus remove"></span></div>';
            $('.appending_div').append(field);
            i = i + 1;

            if (i >= maxGrades) {
                $(this).prop('disabled', true);
            }
        }

        if (i === maxGrades) {
            $(this).hide(); // Hide the plus sign button when the maximum limit is reached
        }
    });

    // Handle removal of fields
    $('.appending_div').on('click', '.remove', function() {
        $(this).parent().remove();
        i = i - 1;

        if (i < maxGrades) {
            $('.add').prop('disabled', false);
            $('.add').show(); // Show the plus sign button when a field is removed
        }

        if (i === 0) {
            $('.add').show(); // Show the plus sign button when all fields are removed
        }
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

       // Check if the total number of questions is greater than 0
      var mcqValue = parseInt($('[name="mcq"]').val()) || 0;
      var msqValue = parseInt($('[name="msq"]').val()) || 0;
      var oaqValue = parseInt($('[name="oaq"]').val()) || 0;
      var totalQuestions = mcqValue + msqValue + oaqValue;

      const userMembershipType = document.getElementById('user_membership').value;
      const userMembershipWords = parseInt(document.getElementById('membership_words').value, 10);
      const userMembershipQuestions = parseInt(document.getElementById('membership_questions').value, 10);
      const userMembershipTests = parseInt(document.getElementById('membership_tests').value, 10);
      const userTestsCountLastMonth = parseInt(document.getElementById('user_test_count_last_month').value, 10);

        var header = $('[name="header"]').val();
        if (header === '') {
        alert('Header field cannot be empty.');
        return;
      }
        if (userTestsCountLastMonth > userMembershipTests) {
            alert('You exceeded the maximum number of tests per month for your plan. Please upgrade.');
        return;
      }
       // Check if the "Teaching Material" field has a value
      var teachingMaterialValue = $('#teaching-material').val().trim();
      if (teachingMaterialValue === '') {
        alert('Teaching Material field cannot be empty.');
        return;
      }
      // Check if the "Teaching Material" field has a length between 100 and 54000 characters
        var splits = teachingMaterialValue.split(/(\s+)/);
        var words = splits.filter((x) => x.trim().length>0);
        var wordCount = words.length;
      if (wordCount < 100) {
        alert('Teaching Material must be more than 100 words.');
        return;
      }
      if (wordCount > userMembershipWords) {
        alert('You exceeded the maximum words allowed for your membership. Please visit Plans to upgrade');
        return;
      }
      if (totalQuestions <= 0) {
        alert('Total questions must be greater than 0.');
        return;
      }
       if (totalQuestions > userMembershipQuestions) {
            alert('You exceeded the maximum number of questions per test for your membership');
        return;
      }

      var WQratio = wordCount / totalQuestions;

      if (WQratio < 100) {
        var userConfirmation = confirm('Too many question for a short text. There are more than 1 questions per 100 words. This might introduce repeated questions. Do you want to continue?');
        if (!userConfirmation) {
            return;
        }
        }

      // Show the overlay and loading animation
      $('#overlay').show();
      $('#loading-animation').show();

      // Send the form data using AJAX
      $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        success: function(response) {
          // Hide the overlay and loading animation
          $('#overlay').hide();
          $('#loading-animation').hide();

          // Redirect to '/my-tests' only upon success and if Teaching Material has a value and total questions > 0
          window.location.href = '/my-tests/home-view/';
        },
        error: function(error) {
          // Handle error if needed
          console.log(error);
          // Hide the overlay and loading animation in case of an error
          $('#overlay').hide();
          $('#loading-animation').hide();
        }
      });

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

  });

    const uploadedFiles = [];

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

      handleFile(event.dataTransfer.files[0]);
    });

    document.getElementById('file-input').addEventListener('change', function (event) {
      handleFile(event.target.files[0]);
    });

    document.getElementById('teaching-material').addEventListener('input', function (event) {
      const teachingMaterialTextarea = event.target;
      uploadedFiles.length = 0;
      const lines = teachingMaterialTextarea.value.split('\n');
      lines.forEach(line => {
        if (line.trim() !== '') {
          uploadedFiles.push(line);
        }
      });
    });

    function handleFile(file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        const teachingMaterialTextarea = document.getElementById('teaching-material');
        const fileType = file.name.split('.').pop().toLowerCase();

        if (fileType === 'docx') {
          mammoth.extractRawText({ arrayBuffer: e.target.result })
            .then((result) => {
              // Preserve new lines from the Word document
              const plainText = result.value.trim();
              teachingMaterialTextarea.value += '\n\n' + plainText;
              uploadedFiles.push(plainText);
            });
        } else if (fileType === 'pdf') {
      const typedArray = new Uint8Array(e.target.result);
      pdfjsLib.getDocument(typedArray).promise.then((pdfDoc) => {
        const numPages = pdfDoc.numPages;
        for (let pageNum = 1; pageNum <= numPages; pageNum++) {
          pdfDoc.getPage(pageNum).then((page) => {
            return page.getTextContent();
          }).then((content) => {
            const pageText = content.items.map(item => item.str).join(' ');
            teachingMaterialTextarea.value += '\n\n' + pageText;
            uploadedFiles.push(pageText);
          });
        }
      });
        } else {
          teachingMaterialTextarea.value += '\n\n' + e.target.result;
          uploadedFiles.push(e.target.result);
        }
      };

            if (file.type === 'text/plain') {
        reader.readAsText(file);
      } else {
        reader.readAsArrayBuffer(file);
      }
    }

  $(document).ready(function() {
    // Intercept form submission
    $('#quick-test-form').on('submit', function(e) {
      e.preventDefault(); // Prevent default form submission

       // Check if the total number of questions is greater than 0
      var mcqValue = parseInt($('[name="mcq"]').val()) || 0;
      var msqValue = parseInt($('[name="msq"]').val()) || 0;
      var oaqValue = parseInt($('[name="oaq"]').val()) || 0;
      var totalQuestions = mcqValue + msqValue + oaqValue;

      const userMembershipType = document.getElementById('user_membership').value;
      const userMembershipWords = parseInt(document.getElementById('membership_words').value, 10);
      const userMembershipQuestions = parseInt(document.getElementById('membership_questions').value, 10);
      const userMembershipTests = parseInt(document.getElementById('membership_tests').value, 10);
      const userTestsCountLastMonth = parseInt(document.getElementById('user_test_count_last_month').value, 10);

//====================== Test eligibility alerts =========================================

        if (userTestsCountLastMonth > userMembershipTests) {
            alert('You exceeded the maximum number of tests per month for your plan. Please upgrade.');
        return;
      }

       // Check if the "Teaching Material" field has a value
      var teachingMaterialValue = $('#teaching-material').val().trim();
      if (teachingMaterialValue === '') {
        alert('Teaching Material field cannot be empty.');
        return;
      }

      // Check if the "Teaching Material" field has a length between 100 and 54000 characters
        var splits = teachingMaterialValue.split(/(\s+)/);
        var words = splits.filter((x) => x.trim().length>0);
        var wordCount = words.length;
      if (wordCount < 100) {
        alert('Teaching Material must be more than 100 words.');
        return;
      }
      if (wordCount > userMembershipWords) {
        alert('Teaching Material must be less than 200,000 words.');
        return;
      }

      if (totalQuestions <= 0) {
        alert('Total questions must be greater than 0.');
        return;
      }

       if (totalQuestions > userMembershipQuestions) {
            alert('You exceeded the maximum number of questions per test for your membership');
        return;
      }

      var WQratio = wordCount / totalQuestions;

      if (WQratio < 100) {
  var userConfirmation = confirm('Too many question for a short text. There are more than 1 questions per 100 words. This might introduce repeated questions. Do you want to continue?');
  if (!userConfirmation) {
    return;
  }
}

//====================== Test eligibility alerts =========================================


      // Show the overlay and loading animation
      $('#overlay').show();
      $('#loading-animation').show();

      // Send the form data using AJAX
      $.ajax({
        url: $(this).attr('action'),
        type: $(this).attr('method'),
        data: $(this).serialize(),
        success: function(response) {
          // Hide the overlay and loading animation
          $('#overlay').hide();
          $('#loading-animation').hide();

          // Redirect to '/my-tests' only upon success and if Teaching Material has a value and total questions > 0
          window.location.href = '/my-tests/home-view/';
        },
        error: function(error) {
          // Handle error if needed
          console.log(error);
          // Hide the overlay and loading animation in case of an error
          $('#overlay').hide();
          $('#loading-animation').hide();
        }
      });
    });
  });


  document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    let deleteUrl = '';

    // Attach click event to all delete buttons
    deleteButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        deleteUrl = btn.getAttribute('data-url');
        $('#confirmationModal').modal('show');
      });
    });

    // Attach click event to confirm delete button in modal
    confirmDeleteBtn.addEventListener('click', function () {
      if (deleteUrl) {
        window.location.href = deleteUrl;
      }
    });
  });









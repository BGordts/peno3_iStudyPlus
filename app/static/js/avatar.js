// Required for drag and drop file access
//jQuery.event.props.push('dataTransfer');

// IIFE to prevent globals
(function () {

	var s;
	var Avatar = {

		settings: {
			bod: document.getElementsByTagName("body")[0],
			img: document.getElementById("profile-avatar"),
			fileInput: document.getElementById("uploader"),
			imageStorage: []
		},

		init: function () {
			s = Avatar.settings;
			Avatar.bindUIActions();
		},

		bindUIActions: function () {

			var timer;

			function dragEnterLeave(event) {
				event.stopPropagation();
				event.preventDefault();
			}
			window.addEventListener("dragenter", dragEnterLeave, false);
			window.addEventListener("dragleave", dragEnterLeave, false);
			window.addEventListener("dragover", function (event) {
				event.stopPropagation()
				event.preventDefault()
				var clazz = 'not-available'
				var ok = event.dataTransfer && event.dataTransfer.types && event.dataTransfer.types.indexOf('Files') >= 0
			}, false)
			window.addEventListener("drop", function (event) {
				console.log('drop event:', JSON.parse(JSON.stringify(event.dataTransfer)))
				event.stopPropagation()
				event.preventDefault()

				Avatar.handleDrop(event.dataTransfer.files);
			}, false)

			s.fileInput.addEventListener('change', function (event) {
				Avatar.handleDrop(event.target.files);
			});
		},

		showDroppableArea: function () {
			//      s.bod.addClass("droppable");
		},
		//
		hideDroppableArea: function () {
			//      s.bod.removeClass("droppable");
		},

		handleDrop: function (files) {

			Avatar.hideDroppableArea();

			// Multiple files can be dropped. Lets only deal with the "first" one.
			var file = files[0];

			if (typeof file !== 'undefined' && file.type.match('image.*')) {

				Avatar.resizeImage(file, 256, function (data) {
					Avatar.placeImage(data);
				});
				Avatar.resizeImage(file, 125, function (data) {
					document.getElementById("profile-img_large").value = data;
				});
				Avatar.resizeImage(file, 32, function (data) {
					document.getElementById("profile-img_small").value = data;
				});


			} else {

				alert("That file wasn't an image.");

			}

		},

		resizeImage: function (file, size, callback) {

			var fileTracker = new FileReader;
			fileTracker.onload = function () {
				Resample(
				this.result,
				size,
				size,
				callback);
			}
			fileTracker.readAsDataURL(file);

			fileTracker.onabort = function () {
				alert("The upload was aborted.");
			}
			fileTracker.onerror = function () {
				alert("An error occured while reading the file.");
			}

		},

		placeImage: function (data) {
			s.img.setAttribute("src", data)
		},

		storeImage: function (data) {
			s.imageStorage.push(data)
			console.log(data)
		}

	}

	Avatar.init();

})();
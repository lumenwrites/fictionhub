import SimpleMDE from 'simplemde';

$(document).ready(function() {
    console.log("Simplemde");
    var editor = $(".editor")[0];
    if (editor) {
	var simplemde = new SimpleMDE({
	    autofocus: true,
	    autosave: {
		enabled: false,
		uniqueId: "MyUniqueID",
		delay: 1000,
	    },
	    insertTexts: {
		horizontalRule: ["", "\n\n-- readmore ---\n\n"],
	    },
	    lineWrapping: false,
	    placeholder: "Write here...",
	    spellChecker: false,
	    status: ["autosave", "words"], // Optional usage
	    status: ["autosave", "words", {
		className: "keystrokes",
		defaultValue: function(el) {
		    this.keystrokes = 0;
		    el.innerHTML = "0 Keystrokes";
		},
		onUpdate: function(el) {
		    el.innerHTML = ++this.keystrokes + " Keystrokes";
		}
	    }]
	});

    }
});

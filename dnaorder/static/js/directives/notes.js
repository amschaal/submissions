var notes = angular.module("notes", ['Models']);
angular.module('main').requires.push("notes")
notes.directive('submissionNotes', function(Note) {
	return {
		restrict: 'AE',
		templateUrl: '/static/templates/notes_container.html',
		scope: {
			submission: '=',
			submissionId:'@'
		},
		controller: function ($scope,$rootScope) {
			var noteHash={};
			$scope.getResponses = function(note){
				if(note)
					return noteHash[note.id];
				else
					return noteHash[null];
			};
			$scope.save = function(note){
				console.log('save',note.submission,note);
				var method = note.id ? '$save' : '$create';
				if (!note.id && !note.public)
					note.send_email = false;
				note[method](function(){Materialize.toast('Note saved',5000)},function(){Materialize.toast('Error saving note',5000)})
			};
			$scope.newNote = function(){
				var note = new Note({
					type:'NOTE',
					submission:$scope.submissionId,
					//created_by:{{request.user.id}},
					send_email: true,
					public: true,
					editing: true,
					parent: null
				})
				$scope.addNote(note);
			};
			$scope.deleteNote = function(note){
				if (note.id && !confirm("Are you sure you want to delete this note and all responses?"))
					return;
				var parent = note.parent;
				var id = note.id;
				var removeFunc = function() {
					for (var i in noteHash[parent]){
						if (noteHash[parent][i].id == id)
							noteHash[parent].splice(i,1);
					}
					Materialize.toast('Note deleted',5000);
				};
				if(!id){
					removeFunc();
					return;
				}
				note.$remove(removeFunc,function(){Materialize.toast('Error deleting note',5000);});
			};
			$scope.reply = function(parent){
				var note = new Note(
						{
							type:'NOTE',
							submission:$scope.submissionId,
							send_email: true,
							public: true,
							editing: true,
							parent: parent.id
						}
				);
				$scope.addNote(note);
			};
			$scope.addNote = function(note){
				console.log(note);
				if(!noteHash[note.parent])
					noteHash[note.parent] = [];
				noteHash[note.parent].push(note);
			};
//			self.newNote = function(){
//				self.notes.push(
//    				new Note({
//        					type:'NOTE',
//        					submission:$scope.submissionId,
//        					//created_by:{{request.user.id}},
//        					emails: null,
//        					public: true
//    					})
//				);
//			};
//			self.saveNote = function(note){
//				var method = note.id ? '$save' : '$create';
//				if (!note.id && !note.public)
//					note.emails = null;
//				note[method](function(){Materialize.toast('Note saved',5000)},function(){Materialize.toast('Error saving note',5000)})
//			};
//			self.deleteNote = function(note){
//				if (!note.id)
//					self.notes.splice(self.notes.indexOf(note),1);
//				else if (confirm('Are you sure you want to delete this note?'))
//					note.$delete(function(){self.notes.splice(self.notes.indexOf(note),1);Materialize.toast('Note deleted',5000);},function(){Materialize.toast('Error deleting note',5000);});
//			};
			$scope.getClasses= function(note){
        		if (!note.public)
        			return 'red lighten-4';
        		if (note.type == 'NOTE')
        			return 'green lighten-4';
        		if (note.type == 'LOG')
        			return 'orange lighten-5';
        	};
        	$scope.getTypeText = function(note){
        		if (!note.public)
        			return 'Note (private)';
        		if (note.type == 'NOTE')
        			return 'Note';
        		if (note.type == 'LOG')
        			return 'Log';
        	}
        	$scope.getEmailsText = function(note){
        		if (note.emails)
        			return '- Emailed to: '+note.emails.join(', ');
        	}
			$scope.notes = Note.query({submission:$scope.submissionId,page_size:100},function() {
				angular.forEach($scope.notes,function(note){
					$scope.addNote(note);
				});
				console.log('hash',noteHash);
			});
		}
	}
});

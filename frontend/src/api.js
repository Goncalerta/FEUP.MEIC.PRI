import axios from "axios";

const BACKEND_HOST = process.env.REACT_APP_BACKEND_HOST || "django";
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT || "8000";

const BACKEND_SERVER = `${BACKEND_HOST}:${BACKEND_PORT}/api/v1.0/`;

async function apiGet(route, payload = {}) {
    // TODO remove mock. django calls should work already but my pc dies when i try to run everything together
    return {
        status: 200,
        data: [
            {
                date: "2007-08-27T00:00:00Z",
                rating: 5.0,
                user_name: "Taka",
                text: "I did it.38 plays, 2 long poems, and 154 sonnets in 2462 onion-paper pages. I read them all. ALL. I think I deserve a self-congratulation for this. Yes. Good job!It took me more than two months of intense reading that toughened my wrists and arms from reading it on the train standing, hardened my heart with stony indifference against people's perplexed and peering gazes thrown at me even to the point of leaning in from the side to see what the hell I'm reading, and made me utterly fearless against any future reference to Shakespeare.From the end of January to today, April 5th, it was a long journey during which time I came out of Shakespearean depths only once to take a quick breather for five days and read one contemporary book. It was a long, long read indeed.So what do I think of his works? Amazing. If you speak English, read them. My favorite comedies are  The Comedy of Errors,  The Midsummer Night's Dream , All's Well That Ends Well, and of course, my absolute favorite, The Merchant of Venice. As for histories, Henry IV part 1&2, Henry V, and Richard III were fascinating and beautiful in myriad aspects. It seems like I'm drawn to wicked villains like Richard III, Shylock, and Barabas (Marlowe's The Jew of Malta), though I didn't absolutely love Iago from Othello for some reason.And tragedies. Oh man. I read Macbeth and Julius Caesar in high school and middle school respectively, but I can say I understood less than 10% of their artistic merit now that I read them again. Macbeth is just a short, sweet, and wicked play with enchanting poetry, and the speeches in  Julius Caesar are just mind-blowing in their poetry and rhetoric. Romeo and Juliet definitely belongs to one of his greatest works. It's got the engaging story, beautiful language, and comic scenes all rolled in one - everything that makes a work of art entertaining and satisfying to people from all walks of life. Cymbeline is also awesome. The ending just so unrealistic that it's unbelievably satisfying. Hamlet is like a given and I don't think I need to say anything about it other than that it rocks.Oh and I really liked this minor play, Titus Andronicus, considered by many critics to be one of his inferior plays. Granted, the beginning is just absolute shit at least plot-wise, but man, it's AWESOME with all that bloody murders and plotting and hatred and violence. It may be poetically inferior to other tragedies, but story-wise, it holds its own among his corpus.I did it!",
                num_likes: 192,
                content_type: "REVIEW",
                id: "100_REVIEW_1",
                _version_: 1751881336776294400,
            },
            {
                date: "2020-07-25T00:00:00Z",
                rating: 4.0,
                user_name: "leynes",
                text: "Ya'll already knew this was coming because I did the same thing for Oscar but these compilations of my reviews are so damn satisfying to me. The Comedies• As You Like It• The Comedy of Errors• Love’s Labour’s Lost• The Merry Wives of Windsor• A Midsummer Nights’ Dream• Much Ado About Nothing• The Taming of the Shrew• Twelfth Night• Two Gentlemen of VeronaThe Tragedies• Coriolanus• Titus Andronicus• Romeo and Juliet• Julius Caesar• Macbeth• Hamlet• King Lear• Othello• Antony and CleopatraThe Histories• King John• Richard II• Henry IV Part 1• Henry IV Part 2• Henry V• Henry VI Part 1• Henry VI Part 2• Henry VI Part 3• Richard III• Henry VIIIThe Late Romances• Cymbeline• Pericles, Prince of Tyre• The Tempest• The Two Noble KinsmenThe Problem Plays• All’s Well That Ends Well• Measure for Measure• The Merchant of Venice• Timon of Athens• Troilus and Cressida• The Winter’s TaleThe Poetry• The Sonnets• A Lover’s Complaint• The Narrative PoemsIt took me four years to finish Willie's entire body of work, and even though there were some ups and downs, ultimately, I am more than happy that I followed through with this project. I learned so much along the way (about literature, about England, about myself, about reviewing books, about researching and doing secondary reading). Willie's works are truly a treasure.",
                num_likes: 143,
                content_type: "REVIEW",
                id: "100_REVIEW_2",
                _version_: 1751881336776294400,
            },
            {
                date: "2017-05-31T00:00:00Z",
                user_name: "Sean Barrs ",
                text: "I plan to read many Shakespeare plays this summer. I won’t complete the full works, but finishing them all is one of my major reading goals. It might take me a few years to do it, but I shall get there eventually!Here’s where I’m up to at the moment:1 Two Gentlemen of Verona  2 Taming of the Shrew 3 Henry VI, part 1 4 Henry VI, part 3  5 Titus Andronicus 6 Henry VI, part 2  7 Richard III 8 The Comedy of Errors 9 Love's Labours Lost10 A Midsummer Night's Dream  11 Romeo and Juliet  12 Richard II 13 King John14 The Merchant of Venice  15 Henry IV, part 116 The Merry Wives of Windsor17 Henry IV, part 218 Much Ado About Nothing19 Henry V20 Julius Caesar21 As You Like It  22 Hamlet  23 Twelfth Night24 Troilus and Cressida  25 Measure for Measure26 Othello27 All's Well That Ends Well28 Timon of Athens29 The Tragedy of King Lear  30 Macbeth   31 Anthony and Cleopatra 32 Pericles, Prince of Tyre33 Coriolanus34 Winter's Tale35 Cymbeline  36 The Tempest 37 Henry VIII38 SonnetsThere's so may greats on this list that I have to read soon!",
                num_likes: 87,
                content_type: "REVIEW",
                id: "100_REVIEW_3",
                _version_: 1751881336776294400,
            },
            {
                date: "2017-09-15T00:00:00Z",
                rating: 5.0,
                user_name: "Darwin8u",
                text: "January:1. Two Gentlemen of Verona (1589–1591) - January 1, 20172 The Taming of the Shrew (1590–1591) - January 5, 20173 Henry VI, Part 2 (1591) - February 1, 2017February:4 Henry VI, Part 3 (1591) - February 3, 2017 5 Henry VI, Part 1 (1591–1592) - January 21, 2017 6 Titus Andronicus (1591–1592) - February 9, 2017 March:7 Richard III (1592–1593) - March 4, 2017 8. The Comedy of Errors (1594) - March 11, 2017 9. Love's Labour's Lost (1594–1595) - March 27, 2017April:10. Richard II (1595) - April 7, 201711. Romeo and Juliet (1595) - April 12, 201712. A Midsummer Night's Dream (1595) - April 21, 2017 May:13. King John (1596) - May 3, 201714. The Merchant of Venice (1596–1597) - May 8, 201715. Henry IV, Part 1 (1596-1597) - May 20, 2017June:16. The Merry Wives of Windsor (1597) - June 20, 201717. Henry IV, Part 2 (1597-1598) - June 24, 201718. Much Ado About Nothing (1598-1599) - June 25, 2017July:19. Henry V (1599) - July 5, 201720. Julius Caesar (1599) - July 10, 201721. As You Like It (1599-1600) - July 26, 2017August:22. Hamlet (1600-1601)- August 12, 201723. Twelfth Night (1601) - August 15, 201724. Troilus and Cressida ((1600–1602) - August 29, 2017September:25. Measure for Measure (1603-1604) - September 6, 201726. Othello (1603-1604) - September 15, 201727. All's Well that Ends Well (1604-1605) - September 12, 2017October:28. King Lear (1605–1606) - October 19, 201729. Timon of Athens (1605–1606) - October 20, 201730. Macbeth (1606) - October 28, 2017November:31. Antony and Cleopatra (1606) - November 17, 201732. Coriolanus (1608) - November 23, 201733. The Winter's Tale (1609–1611) - November 25, 2017December:34. Cymbeline (1610) - December 11, 201735. The Tempest (1610–1611) - December 12, 201736. Henry VIII (1612–1613) - December 16, 2017Other:Pericles, Prince of Tyre (1607–1608) - November 21, 2017The Sonnets (1609) - December 19, 2017 The Two Noble Kinsmen (1613–1614) - December 19, 2017 The Narrative Poems (1593-1594) - December 23, 2017",
                num_likes: 59,
                content_type: "REVIEW",
                id: "100_REVIEW_4",
                _version_: 1751881336776294400,
            },
            {
                date: "2021-08-25T00:00:00Z",
                rating: 5.0,
                user_name: "Zain",
                text: "Blame It On West Side Story…It was nearly the ending of summer, and I was then still eleven. Was playing basketball with my brother and friends. Came into the house for a cold drink and a snack.Heard my sister and her friends making happy sounds. Decided I should investigate. They were watching a movie called “West Side Story.”I heard lots of fun music, saw lots of fun dancing. Although covered in dirt and smelly with sweat, decided to invite myself in and squeezed between two people.Heard about a song called Maria, Jet Song, Tonight, America, Gee, Officer Krupke, I Feel Pretty and others. There was the beautiful Maria (who, strangely enough, didn’t look Puerto Rican). There was a gorgeous man named Bernardo. My tomboy days were over.Dear mother noticed my happy obsession and told me about two young teenagers named Romeo and Juliet. A play written by William Shakespeare. Two kids in love with love 💕.I devoured the book (in between countless views of West Side Story), repeatedly. Time to move on to more Shakespeare.I fell in love with Macbeth and Hamlet, Taming of the Shrew and The Merchant of Venice. Henry V and Henry IV, Parts I and Il.Sonnets and more sonnets, more dramas, more histories and more comedies. With a multitude of clever quotations, I am definitely still in Shakespeare heaven.Now, if you are reading this review and want to read this book, I will tell you that it is definitely worth the money. Lots of books are claiming to have his complete collection, but they always have something lacking.This is very organized and put together very well. The table of contents list EVERYTHING! There’s a section on the plays that are disputed as not written by Shakespeare. A chapter on his life and times. A chapter on his descendants (there aren’t any). A chapter on his rewriting of famous plays from other countries.There is a good biography on him, and loads of research material. Anything you want is probably right in here.Thanks for stopping by my way to read this review. I hope that you have enjoyed your view. I know that you will definitely enjoy this book. $1.99 on Amazon and iBook.Fabulous five stars ✨✨✨✨✨",
                num_likes: 74,
                content_type: "REVIEW",
                id: "100_REVIEW_5",
                _version_: 1751881336776294400,
            },
            {
                date: "2014-01-27T00:00:00Z",
                rating: 5.0,
                user_name: "Ted",
                text: "Have I read this book? Only part of it.Even so, why argue about that rating?See bottom of review for a list of the plays in orderWhat follows is little more than the GoodReads description of the edition pictured. But I feel I can do that, since I wrote the description.This tome includes all 37 of Shakespeare's plays, as well as his poems and sonnets. It was produced \"for college students in the hope that it will help them to understand, appreciate, and enjoy the works for themselves. It is not intended for the scholar ...\"Two-column format throughout.Introductory Material (90 pages):1. The Universality of Shakespeare2. Records of the Life of Shakespeare3. Shakespeare's England4. Elizabethan Drama5. The Elizabethan Playhouse6. The Study of the Text7. The Development of Shakespeare's Art8. Shakespeare and the Critics9. Shakespearean Scholarship and Criticism 1900-1950Plates:16 full-page Halftone Reproductions6 full-page Line Cuts9 pages of Notes on the PlatesThe Plays:Generally in order of writing.Each play has its own IntroductionFootnotes at the bottom of the columns. This makes them both handy and unobtrusive. Liked by this reader.Appendices follow The Poems:30 Appendices in about the same number of pages; these deal with a wide variety of topics, everything from \"The Melancholic Humor\" to \"Cuckolds and Horns\" to \"Hawks and Hawking\".I don't know how it compares with other editions of Shakespeare's works. It is the one I have.Here are Shakespeare's 37 plays, in the order presented in this edition. This is the best guess (at the time the edition was printed) of the order in which they were written, when on my no-longer-young journey I read the play, and links to my review. (It will take several years for this quest to be completed.)1. The First Part of King Henry the Sixth\t 2. The Second Part of King Henry the Sixth\t 3. The Third Part of King Henry the Sixth\t 4. The Tragedy of King Richard the Third _2017_Apr. 5. The Comedy of Errors\t 6. The Tragedy of Titus Andronicus\t 7. The Taming of the Shrew _2017_Apr. 8. The Two Gentlemen of Verona\t 9. Love's Labor's Lost\t 10. The Tragedy of King Richard the Second _2016_Aug. 11. The Tragedy of Romeo and Juliet\t 12. A Midsummer Night's Dream _2014_Feb. 13. The Life and Death of King John _2016_Apr. 14. The Merchant of Venice\t 15. The First Part of King Henry the Fourth\t 16. The Second Part of King Henry the Fourth\t 17. Much Ado About Nothing\t _2016_Jan. 18. The Life of King Henry the Fifth\t 19. As You Like It _2015_Feb. 20. The Tragedy of Julius Caesar _2017_Oct. 21. Twelfth Night; or What You Will\t 22. The Tragedy of Hamlet, Prince of Denmark\t 23. The Merry Wives of Windsor\t 24. The Tragedy of Troilus and Cressida\t 25. All's Well That Ends Well _2015_June 26. The Tragedy of Othello, the Moor of Venice\t 27. Measure For Measure\t 28. The Tragedy of King Lear\t 29. The Tragedy of Macbeth\t 30. The Tragedy of Anthony and Cleopatra\t 31. The Tragedy of Coriolanus\t 32. Timon of Athens\t 33. Pericles _2016_Oct. 34. Cymbeline\t 35. The Winter's Tale\t 36. The Tempest _2017_July 37. The Famous History of the Life of King Henry the Eighth. . . . . . . . . . . . . . . . . . . .Previous review: The Once and Future King T.H. White's Arthurian fantasyRandom review: King John Wm.ShakespeareNext review:  Understanding Power  Noam ChomskyPrevious library review: Verbivoracious Festschrift Vol. 3 The SyllabusNext library review: Shakespeare: The world as stage Bill Bryson",
                num_likes: 42,
                content_type: "REVIEW",
                id: "100_REVIEW_6",
                _version_: 1751881336776294400,
            },
            {
                date: "2016-10-21T00:00:00Z",
                rating: 5.0,
                user_name: "Daniel Cowan",
                text: "Simply put, When you have The Complete Works of William Shakespeare you have one of the best works of literature ever written. I would definitely place it in the top 10 best works of literature of all time. I bought this book at special price from here:https://www.amazon.com/Complete-Works...",
                num_likes: 39,
                content_type: "REVIEW",
                id: "100_REVIEW_7",
                _version_: 1751881336776294400,
            },
            {
                date: "2012-04-23T00:00:00Z",
                rating: 5.0,
                user_name: "midnightfaerie",
                num_likes: 38,
                content_type: "REVIEW",
                id: "100_REVIEW_8",
                text: "Update as of 2022: Last summer I went to a live production in a castle garden of A Midsummer Night's Dream. I've always thought this play overdone a bit like Romeo and Juliet, it's one of the more popular ones, and I think I finally realize why. Shakespeare, without a doubt, is meant to be seen on stage. I can not stress enough how incredibly brilliant this author is with the written play and seeing it acted out on stage gives it a whole new dimension. This play was fantastic and had me laughing and falling in love with Shakespeare all over again. One of the best classical authors ever. And I highly encourage you to see at least one of his plays in your lifetime.Shakespeare as classical writing written when I first started reading Shakespeare:I understand now why I have such a hard time reading Shakespeare. It's not that it's hard to understand. There are enough translations and self help guides to get you through the plot of any of the plays. And once I started reading and translating, I started to get the hang of it, and had fewer words and phrases that I had to look up. No, it's not that. Simply put, it's a play, and not meant to be read. I know there are some who might disagree with me, however, that's my opinion. I revel in the complacency of description and plays don't have it. It is just dialogue. There is nothing to tell you infinitely how a character is feeling or what they're thinking. There's nothing to tell you how the set looks (besides a sometimes small minimalist description). There is nothing to tell how a character looks, are they beautiful? Are they old? Yes, I understand you can infer many of these things from the dialogue which is what you're supposed to do, but to me, there is great room for interpretation, unlike a book, which will describe it for you. Also, after doing a little reading on Shakespeare and the republishing of his works, it seems there are many different conflicting sources of original text, which is why you often find various works with different scripts. I truly believe that Shakespeare meant these to be seen on stage, not read from a page. It's where his genius is best seen and appreciated. That being said, I plan to read each play, then watch a movie rendition of each one. I would also like to list the reasons here that Shakespeare's works are classics instead of going into the same points repeatedly as I review each work. They are classics, I can't dispute it, whether or not I enjoy each individual play or not. And I do believe this is the first time that an author has gotten 8 out of 10 of my Definitions for a Classic. 1. Longevity: He's been around through the ages and I have no doubt we'll be acting out his plays on the moon.2. The magic factor: His stories will pull you in every time. They focus on the aspects of human nature that we all can relate to, so you care about the outcome of the characters.3. Unique: He has an unusual literary style that has made him popular throughout history.4. New Style of Writing: Now I'm stretching it with this one, I know, because anyone who has studied literature knows Shakespeare wasn't the first to use Iambic Pentameter, however I believe he was the first to make it popular. You ask anyone to tell you the first author that comes to mind when you say Iambic Pentameter and they're not going to say Chaucer, they're going to say Shakespeare.5. Huge Following: There isn't a person on the planet who doesn't know who Shakespeare is.6. Controversial: To say his works are controversial is an understatement. The amount of times he's been banned is enough to put him in this category. The reasons for his censorship are diverse but range from vulgarity, to sex, to politics, to excessive use of freedom. (seriously, what does that even mean?)7. Underlying themes: Underlying themes run rampant throughout his works and offer a wide variety of human conditions. Anything from betrayal and love to honour and glory can be seen in his works.8. Substantial Influence: Shakespeare has had influence in every aspect of society from helping to shape the English language (It's all greek to me and tongue-tied - said to have added over 1700 words to the English language) to politics. (Dangers of introducing foreign politics into a city)Works I've read:OthelloRomeo and JulietHamletMacbethMuch Ado About NothingA Midsummer Night's DreamKing LearThe Merchant of VeniceAs You Like ItThe Taming of the ShrewThe Comedy of Errors",
                _version_: 1751881336776294400,
            },
            {
                date: "2016-03-22T00:00:00Z",
                rating: 5.0,
                user_name: "Manny",
                text: "Celebrity Death Match Special: The Complete Works of Shakespeare versus Deep LearningUbergeek Andrej Karpathy had the bright idea of training a recurrent neural network on the complete works of Shakespeare. It produces remarkably good output for an algorithm which not only knows nothing about Shakespeare, but can't even tell a noun from a verb! Here is the first of the two samples he gives:PANDARUS:Alas, I think he shall be come approached and the dayWhen little srain would be attain'd into being never fed,And who is but a chain and subjects of his death,I should not sleep.Second Senator:They are away this miseries, produced upon my soul,Breaking and strongly should be buried, when I perishThe earth and thoughts of many states.DUKE VINCENTIO:Well, your wit is in the care of side and that.Second Lord:They would be ruled after this chamber, andmy fair nues begun out of the fact, to be conveyed,Whose noble souls I'll have the heart of the wars.Clown:Come, sir, I will make did behold your worship.VIOLA:I'll drink it.____________________The Karpathy article is excellent, and if you're at all geeky yourself I strongly recommend looking at it. The examples are impressive: the random Shakespeare is good, but the random algebraic geometry and random Linux kernel code are even better.",
                num_likes: 37,
                content_type: "REVIEW",
                id: "100_REVIEW_9",
                _version_: 1751881336776294400,
            },
        ],
    };

    /* eslint-disable no-unreachable */
    const config = {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    return axios.get(
        `http://${BACKEND_SERVER}${route}`,
        {
            ...payload,
        },
        config
    );
}

async function apiPost(route, payload = {}) {
    const config = {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    return axios.post(
        `http://${BACKEND_SERVER}${route}`,
        {
            ...payload,
        },
        config
    );
}

const api = {
    get: apiGet,
    post: apiPost,
};

export default api;

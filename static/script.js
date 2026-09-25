var intersectsWithViewport = function (el) {
    var { top, bottom } = el.getBoundingClientRect()

    return (top < window.scrollX + window.innerHeight &&
            bottom > window.scrollX)
}

window.addEventListener('load', () => {
    docs = document.querySelectorAll('.site-container')

    docs.forEach(doc => {
        var content = doc.querySelector('.site-content')
        var title = doc.querySelector('.site-title')
        var id = title.id
        var link = document.querySelector(`#${id}-link`)
        var src = content.getAttribute('data-src')
        axios.get(`/fetch?url=${encodeURIComponent(src)}`)
             .then(({ data }) => {
                 if (data['title']) {
                     title.innerHTML = data['title']
                     link.querySelector('a').innerHTML = data['title']
                 }

                 content.innerHTML = data['body']
                 link.classList.add('load-success')
             })
             .catch(error => {
                 var { data } = error.response
                 link.classList.add('load-failure')
                 doc.classList.add('site-load-failure')
                 content.innerHTML = data['body']
             })
    })

    var focused = docs[0]

    window.addEventListener('scroll', () => {
        docs.forEach(doc => {
            var { top } = doc.getBoundingClientRect()
            var { top: currTop } = focused.getBoundingClientRect()

            if (intersectsWithViewport(doc) &&
                (top < currTop || !intersectsWithViewport(focused))) {
                focused = doc
                docId = doc.querySelector('h2').id

                document.querySelectorAll('.focused-link')
                        .forEach(focused => focused.classList.remove('focused-link'))

                document.querySelector(`#${docId}-link`)
                        .classList.add('focused-link')
            }
        })
    })
})

/*
window.addEventListener('load', () => {
    //const urlParams = new URLSearchParams(window.location.search)
    //const throttle = parseInt(urlParams.get('throttle')) || 0

    docs = document.querySelectorAll('.site-container')

    for (let doc of docs) {
        var content = doc.querySelector('.site-content')
        var title = doc.querySelector('.site-title')
        var id = title.id
        var link = document.querySelector(`#${id}-link`)
        var src = content.getAttribute('data-src')
        try {
            const { data } = await axios.get(`/fetch?url=${encodeURIComponent(src)}`)

            if (data['title']) {
                title.innerHTML = data['title']
                link.querySelector('a').innerHTML = data['title']
            }

            content.innerHTML = data['body']
            link.classList.add('load-success')
        } catch (error) {
            var { data } = error.response
            link.classList.add('load-failure')
            doc.classList.add('site-load-failure')
            content.innerHTML = data['body']
        }
        await new Promise(resolve => setTimeout(resolve, throttle*1000))
    }

    var focused = docs[0]

    window.addEventListener('scroll', () => {
        docs.forEach(doc => {
            var { top } = doc.getBoundingClientRect()
            var { top: currTop } = focused.getBoundingClientRect()

            if (intersectsWithViewport(doc) &&
                (top < currTop || !intersectsWithViewport(focused))) {
                focused = doc
                docId = doc.querySelector('h2').id

                document.querySelectorAll('.focused-link')
                        .forEach(focused => focused.classList.remove('focused-link'))

                document.querySelector(`#${docId}-link`)
                        .classList.add('focused-link')
            }
        })
    })
})
*/
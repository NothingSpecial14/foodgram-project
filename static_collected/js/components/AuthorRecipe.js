class AuthorRecipe extends MainCards{
    constructor(container, card, counter, api, userAuth,button) {
        super(container, card, counter, api, userAuth,button);
    }

    _eventUserAuth (e) {
        super._eventUserAuth(e);
        if (this.target && this.target.name === 'purchases') {
            this._eventPurchases(this.target)
        }
        if (this.target && this.target.name === 'favorites') {
            this._eventFavorites(this.target);
        }
        if (this.target && this.target.name === 'subscribe') {
            this._eventSubscribe(this.target)
        }
    }
    _eventUserNotAuth  (e)  {
        super._eventUserAuth(e);
        if (this.target && this.target.name === 'purchases') {
            this._eventPurchases(this.target)
        }
    }
    _eventSubscribe  (target)  {
        const authorId = target.closest(this.card).getAttribute('data-author');
        if(target.hasAttribute('data-out')) {
            this.button.subscribe.addSubscribe(target, authorId)
        } else {
            this.button.subscribe.removeSubscribe(target,authorId)
        }
    }
    _eventFavorites  (target)  {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.favorites.addFavorites(target,cardId, () => this.tooltipDel(target))
        } else {
            this.button.favorites.removeFavorites(target,cardId, () => this.tooltipAdd(target))
        }
    }
    tooltipAdd  (target) {
        if (!target) {
            console.error('target is null or undefined');
            return;
        }
        const parent = target.closest('.single-card');
        if (!parent) {
            console.error('Parent element with class .single-card not found');
            return;
        }
        const item = parent.querySelector('.single-card__favorite-tooltip');
        if (!item) {
            console.error('Element with class .single-card__favorite-tooltip not found inside parent');
            return;
        }
        item.textContent = "Добавить в избранное";
    }
        
    tooltipDel (target) {
        if (!target) {
            console.error('target is null or undefined');
            return;
        }
        const parent = target.closest('.single-card');
        if (!parent) {
            console.error('Parent element with class .single-card not found');
            return;
        }
        const item = parent.querySelector('.single-card__favorite-tooltip');
        if (!item) {
            console.error('Element with class .single-card__favorite-tooltip not found inside parent');
            return;
        }
        item.textContent = "Убрать из избранного";
    }
        
    _eventPurchases  (target)  {
        const cardId = target.closest(this.card).getAttribute('data-id');
        if(target.hasAttribute('data-out')) {
            this.button.purchases.addPurchases(target,cardId,this.counter.plusCounter)
        } else {
            this.button.purchases.removePurchases(target,cardId,this.counter.minusCounter)
        }
    }
}


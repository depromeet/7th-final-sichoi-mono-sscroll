import { observable } from 'mobx';
import ItemStore from 'store/item';

interface ModelConstructor {
  id: number;
  title: string;
  body: string;
}

export default class ItemModel {
  id: number;
  @observable title: string;
  @observable content: string;

  constructor({ id, title, body }: ModelConstructor) {
    this.id = id;
    this.title = title;
    this.content = body;
  }

  read = () => {
    ItemStore.read(this.id);
  };
}

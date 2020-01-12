import { observable } from 'mobx';

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
}

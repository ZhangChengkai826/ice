(function ($) {
    var dragOffsetX = 0;        //�ؼ���߽�����X��Ĳ�
    var dragOffsetY = 0;        //�ؼ��ϱ߽�����Y��Ĳ�

    $.fn.freeDrag = function () {
        this.mousedown(function (e) {
            //��ȡ���͸ÿؼ���λ��ƫ������������ȫ�ֱ�������������
            dragOffsetX = e.clientX - e.currentTarget.offsetLeft;
            dragOffsetY = e.clientY - e.currentTarget.offsetTop;
        });

        this[0].ondragend = this[0].ondrag = function (e) {
            //���ϻ�ȡ����µ����꣬��������ؼ���������
            var newX = e.clientX - dragOffsetX;
            var newY = e.clientY - dragOffsetY;

            //�߽���ƣ�document.documentElement.clientWidth���ɼ�������  document.documentElement.clientHeight���ɼ�����߶�
            newX = newX < 0 ? 0 : newX;
            newY = newY < 0 ? 0 : newY;
            newX = newX > (document.documentElement.clientWidth - this.width) ? (document.documentElement.clientWidth - this.width) : newX;
            newY = newY > (document.documentElement.clientHeight - this.height) ? (document.documentElement.clientHeight - this.height) : newY;

            //���µ��������¸�ֵ���ؼ�
            $(this).css({ left: newX + "px", top: newY + "px", position: 'absolute' });
        };
    };
})(jQuery);